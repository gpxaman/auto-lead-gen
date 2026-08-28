"""
Provenance trace helper. Per Step 3 Section 44: verify
  OBSERVATION -> RAW RECORD -> INGESTION ITEM -> INGESTION RUN -> SOURCE -> CONNECTOR ->
  CONNECTOR VERSION -> CONFIGURATION
is fully traceable, implementing docs/database/provenance.md's chain concretely.
"""
from dataclasses import dataclass
from typing import Optional

from src.observations.store import ObservationStore
from src.raw.store import IngestionItemStore, IngestionRunStore, RawRecordStore
from src.sources.registry import SourceRegistry


@dataclass
class ProvenanceTrace:
    observation_id: str
    raw_record_id: Optional[str]
    ingestion_item_id: Optional[str]
    ingestion_run_id: Optional[str]
    source_id: Optional[str]
    connector_id: Optional[str]
    connector_version: Optional[str]
    configuration_version: Optional[str]
    complete: bool
    missing_links: list[str]


def trace_observation(
    observation_id: str,
    observation_store: ObservationStore,
    raw_store: RawRecordStore,
    item_store: IngestionItemStore,
    run_store: IngestionRunStore,
    source_registry: SourceRegistry,
) -> ProvenanceTrace:
    missing: list[str] = []

    observation = observation_store.get(observation_id)
    if observation is None:
        return ProvenanceTrace(observation_id, None, None, None, None, None, None, None, False, ["observation"])

    raw_record = raw_store.get(observation.raw_record_id)
    if raw_record is None:
        missing.append("raw_record")

    ingestion_item_id = observation.provenance.get("ingestion_item_id") if observation.provenance else None
    ingestion_item = item_store.get(ingestion_item_id) if ingestion_item_id else None
    if ingestion_item is None:
        missing.append("ingestion_item")

    ingestion_run_id = ingestion_item.ingestion_run_id if ingestion_item else None
    ingestion_run = run_store.get(ingestion_run_id) if ingestion_run_id else None
    if ingestion_run is None:
        missing.append("ingestion_run")

    source = source_registry.get_source(observation.source_id)
    if source is None:
        missing.append("source")

    connector_id = ingestion_run.connector_id if ingestion_run else None
    connector_version = ingestion_run.connector_version if ingestion_run else None
    if connector_id is None:
        missing.append("connector")

    configuration_version = ingestion_run.configuration_version if ingestion_run else None
    if configuration_version is None:
        missing.append("configuration_version")

    return ProvenanceTrace(
        observation_id=observation_id,
        raw_record_id=observation.raw_record_id,
        ingestion_item_id=ingestion_item_id,
        ingestion_run_id=ingestion_run_id,
        source_id=observation.source_id,
        connector_id=connector_id,
        connector_version=connector_version,
        configuration_version=configuration_version,
        complete=(len(missing) == 0),
        missing_links=missing,
    )
