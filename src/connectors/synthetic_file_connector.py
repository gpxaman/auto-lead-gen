"""
SyntheticFileConnector -- per Step 3 Section 40. Reads deterministic fixture data from
tests/fixtures/ingestion/. Used ONLY for testing; never touches a real platform, never contains
real client data. All fixture files are marked SYNTHETIC internally (see the fixtures themselves).
"""
import json
from pathlib import Path

from src.connectors.base import Connector, ConnectorType, RawFetchResult


class SyntheticFileConnector(Connector):
    connector_type = ConnectorType.FILE

    def __init__(self, fixtures_dir: Path):
        self.fixtures_dir = Path(fixtures_dir)
        if not self.fixtures_dir.exists():
            raise FileNotFoundError(f"synthetic fixtures directory not found: {self.fixtures_dir}")

    def discover(self) -> list[str]:
        """One source_identifier per fixture file, keyed by filename stem."""
        return sorted(p.stem for p in self.fixtures_dir.iterdir() if p.is_file())

    def fetch(self, source_identifier: str) -> RawFetchResult:
        matches = list(self.fixtures_dir.glob(f"{source_identifier}.*"))
        if not matches:
            raise FileNotFoundError(f"no fixture found for source_identifier={source_identifier!r}")
        path = matches[0]
        raw_bytes = path.read_bytes()

        content_type = {
            ".json": "application/json",
            ".txt": "text/plain",
            ".html": "text/html",
        }.get(path.suffix, "application/octet-stream")

        if content_type == "application/json":
            try:
                payload = json.loads(raw_bytes.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Malformed JSON fixture: preserve the RAW TEXT exactly, do not discard it
                # (Step 3's Absolute Rule -- malformed content must never be discarded).
                payload = raw_bytes.decode("utf-8", errors="replace")
                content_type = "text/plain"  # honest about what we could actually parse it as
        else:
            payload = raw_bytes.decode("utf-8", errors="replace")

        return RawFetchResult(
            source_identifier=source_identifier,
            raw_payload=payload,
            content_type=content_type,
            source_url=f"synthetic://fixtures/{path.name}",
            request_metadata={"fixture_path": str(path)},
            response_metadata={"file_size_bytes": len(raw_bytes)},
        )
