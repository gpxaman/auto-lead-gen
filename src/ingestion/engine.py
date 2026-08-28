"""
Ingestion Engine -- the orchestrator implementing Step 3's full conceptual flow (Section 60):

  SOURCE -> SOURCE REGISTRY -> CONNECTOR -> INGESTION RUN -> INGESTION ITEM -> RAW RECORD ->
  HASH / VERSION CHECK -> SECURITY INSPECTION -> QUARANTINE OR PROCESS -> NORMALIZATION ->
  OBSERVATION -> (FUTURE CLASSIFICATION, out of scope)

Deterministic and controllable throughout (Step 3 Section 58) -- no LLM call exists anywhere in
this module or anything it calls. Every step preserves raw data per the Absolute Rule: nothing is
summarized, rewritten, or discarded; unknown/malformed/quarantined/duplicate/failed items all
still receive a permanent, auditable identity.
"""
from dataclasses import replace
from datetime import datetime, timezone
from typing import Optional

from src.common.events import EventLog, make_event
from src.common.health import HealthResult, HealthStatus, simple_health
from src.common.ids import new_id
from src.common.logging_utils import log_structured
from src.connectors.base import Connector
from src.ingestion.envelope import build_envelope
from src.ingestion.lead_candidate import LEAD_CANDIDATE_OBSERVATION_TYPE
from src.observations.models import new_observation
from src.observations.normalizer import normalize
from src.observations.store import ObservationStore
from src.quarantine.store import QuarantineStore
from src.raw.models import (
    DuplicateStatus,
    FailureReason,
    IngestionItem,
    IngestionRun,
    IngestionRunStatus,
    ProcessingStatus,
    SecurityStatus,
)
from src.raw.store import IngestionItemStore, IngestionRunStore, RawRecordStore
from src.schemas.detection import detect_schema
from src.security.inspector import SecurityVerdict, inspect
from src.sources.registry import SourceRegistry

QUARANTINE_VERDICTS = (SecurityVerdict.SUSPICIOUS, SecurityVerdict.MALICIOUS)


class IngestionEngine:
    def __init__(
        self,
        source_registry: SourceRegistry,
        raw_store: RawRecordStore,
        run_store: IngestionRunStore,
        item_store: IngestionItemStore,
        observation_store: ObservationStore,
        quarantine_store: QuarantineStore,
        event_log: EventLog,
        configuration_version: str = "CONFIG-V1",
    ):
        self.source_registry = source_registry
        self.raw_store = raw_store
        self.run_store = run_store
        self.item_store = item_store
        self.observation_store = observation_store
        self.quarantine_store = quarantine_store
        self.event_log = event_log
        self.configuration_version = configuration_version

    def run_ingestion(
        self,
        source_id: str,
        connector: Connector,
        connector_id: str,
        connector_version: str,
        correlation_id: Optional[str] = None,
        identifiers: Optional[list[str]] = None,
    ) -> IngestionRun:
        """
        Execute one full ingestion run against a connector. `identifiers`, if given, restricts
        processing to those source_identifiers (for testing specific fixtures); otherwise
        connector.discover() is used.
        """
        run = IngestionRun(
            ingestion_run_id=new_id("run-"),
            source_id=source_id,
            connector_id=connector_id,
            connector_version=connector_version,
            started_at=datetime.now(timezone.utc).isoformat(),
            status=IngestionRunStatus.STARTED,
            configuration_version=self.configuration_version,
            correlation_id=correlation_id or new_id("corr-"),
        )
        self.run_store.save(run)
        self.event_log.append(make_event(
            event_type="IngestionStarted", aggregate_type="ingestion_run", aggregate_id=run.ingestion_run_id,
            producer="IngestionEngine", payload={"source_id": source_id, "connector_id": connector_id},
            correlation_id=run.correlation_id,
        ))
        log_structured("ingestion_started", ingestion_run_id=run.ingestion_run_id, source_id=source_id, connector_id=connector_id)

        run.status = IngestionRunStatus.RUNNING
        self.run_store.save(run)

        to_process = identifiers if identifiers is not None else connector.discover()
        any_failure = False
        any_success = False

        for source_identifier in to_process:
            run.records_received += 1
            try:
                outcome = self._process_one_item(run, connector, source_identifier)
                if outcome == "FAILED":
                    any_failure = True
                    run.records_failed += 1
                else:
                    any_success = True
                    if outcome == "QUARANTINED":
                        run.records_quarantined += 1
                    elif outcome == "DUPLICATE":
                        run.records_duplicated += 1
                    else:
                        run.records_accepted += 1
            except Exception as exc:  # a single item's unexpected failure must not lose the rest of the run
                any_failure = True
                run.records_failed += 1
                self._record_failed_item(run, source_identifier, FailureReason.STORAGE_FAILURE, str(exc))

            self.run_store.save(run)  # persist counters incrementally -- partial progress is never lost

        run.completed_at = datetime.now(timezone.utc).isoformat()
        if any_failure and any_success:
            run.status = IngestionRunStatus.PARTIAL
        elif any_failure and not any_success:
            run.status = IngestionRunStatus.FAILED
        else:
            run.status = IngestionRunStatus.COMPLETED
        self.run_store.save(run)

        completion_event_type = "IngestionCompleted" if run.status == IngestionRunStatus.COMPLETED else "IngestionFailed"
        self.event_log.append(make_event(
            event_type=completion_event_type, aggregate_type="ingestion_run", aggregate_id=run.ingestion_run_id,
            producer="IngestionEngine",
            payload={"status": run.status.value, "records_received": run.records_received, "records_accepted": run.records_accepted,
                     "records_quarantined": run.records_quarantined, "records_failed": run.records_failed, "records_duplicated": run.records_duplicated},
            correlation_id=run.correlation_id,
        ))
        log_structured("ingestion_completed", ingestion_run_id=run.ingestion_run_id, status=run.status.value,
                        received=run.records_received, accepted=run.records_accepted,
                        quarantined=run.records_quarantined, failed=run.records_failed, duplicated=run.records_duplicated)
        return run

    # -- Per-item pipeline -----------------------------------------------------

    def _process_one_item(self, run: IngestionRun, connector: Connector, source_identifier: str) -> str:
        """Returns one of: ACCEPTED, QUARANTINED, DUPLICATE, FAILED."""
        item = IngestionItem(
            ingestion_item_id=new_id("item-"),
            ingestion_run_id=run.ingestion_run_id,
            source_id=run.source_id,
            received_at=datetime.now(timezone.utc).isoformat(),
            observed_at=datetime.now(timezone.utc).isoformat(),
            content_type="unknown",
        )
        self.item_store.save(item)

        try:
            fetch_result = connector.fetch(source_identifier)
            fetch_result = connector.parse(fetch_result)
        except Exception as exc:
            item.processing_status = ProcessingStatus.FAILED
            item.failure_reason = FailureReason.NETWORK_FAILURE
            item.error_reference = str(exc)
            self.item_store.save(item)
            self.event_log.append(make_event(
                event_type="RawRecordReceived", aggregate_type="ingestion_item", aggregate_id=item.ingestion_item_id,
                producer="IngestionEngine", payload={"status": "FAILED", "reason": "NETWORK_FAILURE", "detail": str(exc)},
                correlation_id=run.correlation_id,
            ))
            return "FAILED"

        item.content_type = fetch_result.content_type
        content_hash, duplicate_status, existing_record_id = self.raw_store.classify_incoming(
            run.source_id, source_identifier, fetch_result.raw_payload, fetch_result.content_type
        )
        item.content_hash = content_hash.hash
        item.duplicate_status = duplicate_status

        if duplicate_status == DuplicateStatus.EXACT_DUPLICATE:
            # Per Step 3 Section 15: link to the existing raw record, do NOT create a new one,
            # but the incoming observation event itself remains auditable (a new IngestionItem
            # row + event was already created above -- it is never discarded).
            item.raw_record_id = existing_record_id
            item.processing_status = ProcessingStatus.RECEIVED
            self.item_store.save(item)
            self.event_log.append(make_event(
                event_type="RawRecordReceived", aggregate_type="ingestion_item", aggregate_id=item.ingestion_item_id,
                producer="IngestionEngine",
                payload={"status": "EXACT_DUPLICATE", "existing_raw_record_id": existing_record_id, "source_identifier": source_identifier},
                correlation_id=run.correlation_id,
                idempotency_key=f"{run.source_id}:{source_identifier}:{content_hash.hash}",
            ))
            log_structured("raw_record_duplicate", ingestion_item_id=item.ingestion_item_id, source_id=run.source_id, existing_raw_record_id=existing_record_id)
            return "DUPLICATE"

        # New raw record (first observation OR a changed version of a known source_identifier)
        prior_chain = self.raw_store.get_version_chain(run.source_id, source_identifier)
        is_new_version = len(prior_chain) > 0

        record = self.raw_store.store_new_version(
            record_id=new_id("rr-"),
            source_id=run.source_id,
            ingestion_item_id=item.ingestion_item_id,
            source_identifier=source_identifier,
            raw_payload=fetch_result.raw_payload,
            content_type=fetch_result.content_type,
            content_hash=content_hash.hash,
            retrieved_at=fetch_result.retrieved_at,
            observed_at=item.observed_at,
            source_url=fetch_result.source_url,
            request_metadata=fetch_result.request_metadata,
            response_metadata=fetch_result.response_metadata,
            retrieval_method=connector.connector_type.value,
            connector_version=run.connector_version,
        )
        item.raw_record_id = record.record_id

        self.event_log.append(make_event(
            event_type=("RawRecordVersioned" if is_new_version else "RawRecordReceived"),
            aggregate_type="raw_record", aggregate_id=record.record_id, producer="IngestionEngine",
            payload={"source_identifier": source_identifier, "supersedes": record.supersedes_raw_record_id, "content_hash": content_hash.hash},
            correlation_id=run.correlation_id,
            idempotency_key=f"{run.source_id}:{source_identifier}:{content_hash.hash}",
        ))
        log_structured("raw_record_stored", ingestion_item_id=item.ingestion_item_id, raw_record_id=record.record_id,
                        is_new_version=is_new_version, source_id=run.source_id)

        # -- Security inspection (deterministic; separate from raw payload) --------------------
        security_result = inspect(fetch_result.raw_payload)
        item.security_status = SecurityStatus(security_result.verdict.value)
        record.security_status = SecurityStatus(security_result.verdict.value)

        if security_result.verdict in QUARANTINE_VERDICTS:
            reason = "; ".join(d["pattern_type"] for d in security_result.detections) or "unspecified"
            qrecord = self.quarantine_store.quarantine(
                raw_record_id=record.record_id,
                reason=reason,
                detection_type=(security_result.detections[0]["pattern_type"] if security_result.detections else "UNSPECIFIED"),
                detector=security_result.detector,
                detector_version=security_result.detector_version,
                severity=security_result.verdict.value,
            )
            item.processing_status = ProcessingStatus.QUARANTINED
            self.item_store.save(item)
            self.event_log.append(make_event(
                event_type="RawRecordQuarantined", aggregate_type="raw_record", aggregate_id=record.record_id,
                producer="IngestionEngine",
                payload={"quarantine_id": qrecord.quarantine_id, "reason": reason, "verdict": security_result.verdict.value,
                         "detections": security_result.detections},
                correlation_id=run.correlation_id,
            ))
            log_structured("raw_record_quarantined", ingestion_item_id=item.ingestion_item_id, raw_record_id=record.record_id,
                            quarantine_id=qrecord.quarantine_id, verdict=security_result.verdict.value)
            return "QUARANTINED"

        # -- Schema detection + normalization (SAFE/UNKNOWN verdicts proceed) ------------------
        schema_result = detect_schema(fetch_result.raw_payload)
        item.schema_status = schema_result.schema_status
        record.schema_version = schema_result.schema_version

        normalization_result = normalize(fetch_result.raw_payload, schema_result)
        item.processing_status = ProcessingStatus.NORMALIZED
        self.item_store.save(item)

        observation_type = LEAD_CANDIDATE_OBSERVATION_TYPE if schema_result.schema_status.value in ("KNOWN", "KNOWN_LEGACY", "PARTIAL") else "unknown_content"
        observation = new_observation(
            source_id=run.source_id,
            raw_record_id=record.record_id,
            observed_at=item.observed_at,
            observation_type=observation_type,
            normalized_payload=normalization_result.normalized_payload,
            subject_reference=source_identifier,
            provenance={
                "ingestion_run_id": run.ingestion_run_id,
                "ingestion_item_id": item.ingestion_item_id,
                "connector_id": run.connector_id,
                "connector_version": run.connector_version,
                "configuration_version": run.configuration_version,
                "schema_detection": {"schema_name": schema_result.schema_name, "schema_version": schema_result.schema_version, "schema_status": schema_result.schema_status.value},
                "security_analysis_id": security_result.analysis_id,
            },
        )
        self.observation_store.save(observation)

        self.event_log.append(make_event(
            event_type="ObservationCreated", aggregate_type="observation", aggregate_id=observation.observation_id,
            producer="IngestionEngine",
            payload={"raw_record_id": record.record_id, "observation_type": observation_type, "schema_status": schema_result.schema_status.value},
            correlation_id=run.correlation_id,
        ))
        log_structured("observation_created", ingestion_item_id=item.ingestion_item_id, observation_id=observation.observation_id,
                        observation_type=observation_type, schema_status=schema_result.schema_status.value)
        return "ACCEPTED"

    def _record_failed_item(self, run: IngestionRun, source_identifier: str, reason: FailureReason, detail: str) -> None:
        item = IngestionItem(
            ingestion_item_id=new_id("item-"),
            ingestion_run_id=run.ingestion_run_id,
            source_id=run.source_id,
            received_at=datetime.now(timezone.utc).isoformat(),
            observed_at=datetime.now(timezone.utc).isoformat(),
            content_type="unknown",
            processing_status=ProcessingStatus.FAILED,
            failure_reason=reason,
            error_reference=detail,
        )
        self.item_store.save(item)
        self.event_log.append(make_event(
            event_type="IngestionFailed", aggregate_type="ingestion_item", aggregate_id=item.ingestion_item_id,
            producer="IngestionEngine", payload={"source_identifier": source_identifier, "reason": reason.value, "detail": detail},
            correlation_id=run.correlation_id,
        ))

    # -- Replay (Step 3 Section 32) ---------------------------------------------------------

    def replay(self, raw_record_id: str, normalizer_version: str = "2.0") -> "Observation":  # noqa: F821
        """
        Reprocess an existing, UNCHANGED raw record through normalization again (e.g. with a new
        normalizer version). Produces a NEW Observation; the original raw record and its original
        Observation(s) are untouched (Step 3 Sections 32-33).
        """
        from src.observations.models import new_observation as _new_observation  # local import avoids cycle at module load

        record = self.raw_store.get(raw_record_id)
        if record is None:
            raise KeyError(f"unknown raw_record_id: {raw_record_id}")

        schema_result = detect_schema(record.raw_payload)
        normalization_result = normalize(record.raw_payload, schema_result)
        observation = _new_observation(
            source_id=record.source_id,
            raw_record_id=record.record_id,
            observed_at=record.observed_at,
            observation_type=LEAD_CANDIDATE_OBSERVATION_TYPE if schema_result.schema_status.value in ("KNOWN", "KNOWN_LEGACY", "PARTIAL") else "unknown_content",
            normalized_payload=normalization_result.normalized_payload,
            subject_reference=record.source_identifier,
            normalizer_version=normalizer_version,
            provenance={
                "ingestion_item_id": record.ingestion_item_id,
                "replay": True,
                "replayed_from_raw_record_id": raw_record_id,
                "schema_detection": {"schema_name": schema_result.schema_name, "schema_version": schema_result.schema_version, "schema_status": schema_result.schema_status.value},
            },
        )
        self.observation_store.save(observation)
        self.event_log.append(make_event(
            event_type="ObservationCreated", aggregate_type="observation", aggregate_id=observation.observation_id,
            producer="IngestionEngine.replay", payload={"raw_record_id": raw_record_id, "normalizer_version": normalizer_version, "replay": True},
        ))
        return observation

    def health_check(self) -> HealthResult:
        return simple_health("ingestion_engine", HealthStatus.HEALTHY, detail=f"{len(self.run_store.all())} runs executed")
