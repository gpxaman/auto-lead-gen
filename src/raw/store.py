"""
Raw record / ingestion run / ingestion item stores.

DEVELOPMENT_ONLY in-memory implementation -- see docs/database/schema.sql's header for why no
production database vendor is selected (docs/architecture/open-decisions.md #7). This class
implements the SAME logical guarantees a real backend would need to provide: append-only raw
storage, version chaining via supersedes_raw_record_id, and content-hash-based duplicate
detection -- exactly the rules in docs/database/integrity-rules.md, just backed by Python
dictionaries instead of a real database engine for Step 3's deterministic, controllable pipeline.
"""
from typing import Optional

from src.common.hashing import compute_content_hash
from src.common.health import HealthResult, HealthStatus, simple_health
from src.raw.models import DuplicateStatus, IngestionItem, IngestionRun, RawRecord


class RawRecordStore:
    """
    Append-only. No update()/delete() method exists for record content -- only append_version(),
    which creates a NEW row and links it via supersedes_raw_record_id. This is the concrete
    enforcement of "RAW IS NEVER OVERWRITTEN" (Step 3's Absolute Rule).
    """

    def __init__(self):
        self._records: dict[str, RawRecord] = {}
        # (source_id, source_identifier, content_hash) -> record_id, for exact-duplicate detection
        self._dedup_index: dict[tuple[str, str, str], str] = {}
        # (source_id, source_identifier) -> list of record_ids in chronological order (version chain)
        self._version_chains: dict[tuple[str, str], list[str]] = {}

    def classify_incoming(self, source_id: str, source_identifier: str, raw_payload, content_type: str):
        """
        Per Step 3 Section 14-15: compare content hashes BEFORE deciding whether this is a new
        version, an exact duplicate, or a distinct record. Returns (content_hash, duplicate_status,
        existing_record_id_or_None).
        """
        content_hash = compute_content_hash(raw_payload, content_type)
        key = (source_id, source_identifier, content_hash.hash)
        if key in self._dedup_index:
            return content_hash, DuplicateStatus.EXACT_DUPLICATE, self._dedup_index[key]

        chain_key = (source_id, source_identifier)
        prior_chain = self._version_chains.get(chain_key, [])
        if prior_chain:
            # Same source_identifier, but a DIFFERENT hash than any prior version we've seen ->
            # this is a legitimate content change, not a duplicate. DISTINCT_RECORD (new version).
            return content_hash, DuplicateStatus.DISTINCT_RECORD, None

        return content_hash, DuplicateStatus.DISTINCT_RECORD, None

    def store_new_version(
        self,
        record_id: str,
        source_id: str,
        ingestion_item_id: str,
        source_identifier: str,
        raw_payload,
        content_type: str,
        content_hash: str,
        retrieved_at: str,
        observed_at: str,
        source_url: Optional[str] = None,
        request_metadata: Optional[dict] = None,
        response_metadata: Optional[dict] = None,
        retrieval_method: Optional[str] = None,
        connector_version: Optional[str] = None,
        schema_version: Optional[str] = None,
    ) -> RawRecord:
        chain_key = (source_id, source_identifier)
        prior_chain = self._version_chains.get(chain_key, [])
        supersedes = prior_chain[-1] if prior_chain else None

        record = RawRecord(
            record_id=record_id,
            source_id=source_id,
            ingestion_item_id=ingestion_item_id,
            source_identifier=source_identifier,
            raw_payload=raw_payload,
            content_type=content_type,
            content_hash=content_hash,
            retrieved_at=retrieved_at,
            observed_at=observed_at,
            source_url=source_url,
            request_metadata=request_metadata,
            response_metadata=response_metadata,
            retrieval_method=retrieval_method,
            connector_version=connector_version,
            schema_version=schema_version,
            supersedes_raw_record_id=supersedes,
        )
        self._records[record_id] = record
        self._dedup_index[(source_id, source_identifier, content_hash)] = record_id
        self._version_chains.setdefault(chain_key, []).append(record_id)
        return record

    def get(self, record_id: str) -> Optional[RawRecord]:
        return self._records.get(record_id)

    def get_version_chain(self, source_id: str, source_identifier: str) -> list[RawRecord]:
        """Full, ordered, un-truncated version history for one (source, source_identifier) pair."""
        ids = self._version_chains.get((source_id, source_identifier), [])
        return [self._records[i] for i in ids]

    def get_latest_version(self, source_id: str, source_identifier: str) -> Optional[RawRecord]:
        chain = self.get_version_chain(source_id, source_identifier)
        return chain[-1] if chain else None

    def all(self) -> list[RawRecord]:
        return list(self._records.values())

    def health_check(self) -> HealthResult:
        return simple_health("raw_record_store", HealthStatus.HEALTHY, detail=f"{len(self._records)} raw records stored")


class IngestionRunStore:
    def __init__(self):
        self._runs: dict[str, IngestionRun] = {}

    def save(self, run: IngestionRun) -> None:
        """Upsert by ingestion_run_id -- this IS the single mutable-status entity in the pipeline
        (a run's status legitimately progresses STARTED -> RUNNING -> COMPLETED/PARTIAL/FAILED),
        but the run row itself is never deleted, including FAILED/CANCELLED runs (Step 3 Section 10:
        'Never erase failed runs')."""
        self._runs[run.ingestion_run_id] = run

    def get(self, ingestion_run_id: str) -> Optional[IngestionRun]:
        return self._runs.get(ingestion_run_id)

    def all(self) -> list[IngestionRun]:
        return list(self._runs.values())

    def by_source(self, source_id: str) -> list[IngestionRun]:
        return [r for r in self._runs.values() if r.source_id == source_id]


class IngestionItemStore:
    def __init__(self):
        self._items: dict[str, IngestionItem] = {}

    def save(self, item: IngestionItem) -> None:
        self._items[item.ingestion_item_id] = item

    def get(self, ingestion_item_id: str) -> Optional[IngestionItem]:
        return self._items.get(ingestion_item_id)

    def all(self) -> list[IngestionItem]:
        return list(self._items.values())

    def by_run(self, ingestion_run_id: str) -> list[IngestionItem]:
        return [i for i in self._items.values() if i.ingestion_run_id == ingestion_run_id]
