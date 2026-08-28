# Connector Interface

Per Step 3 Sections 8, 38-40. Implementation: `src/connectors/base.py`,
`src/connectors/synthetic_file_connector.py`. Tests: `tests/connectors/test_synthetic_connector.py`.

## The abstraction, not 46 scrapers (Step 3 Section 38)

Only the `Connector` ABC and ONE synthetic implementation exist. No live platform connector
(Upwork, Alibaba, etc.) is built in Step 3 — future connectors plug into the same
`discover()`/`fetch()`/`parse()` interface without touching `src/ingestion/engine.py`.

## What a connector may NOT do (Step 3 Section 39) — enforced by interface shape

`RawFetchResult` (the only object a connector may return from `fetch()`) has exactly 7 fields:
`source_identifier`, `raw_payload`, `content_type`, `source_url`, `request_metadata`,
`response_metadata`, `retrieved_at`. There is no field for a classification, a business decision,
or evidence rewriting — a connector CANNOT express those things through this interface even if it
tried. Verified in `test_connector_does_not_classify_or_judge`.

## `ConnectorType` (Step 3 Section 8)

`API | WEB | RSS | FILE | WEBHOOK | MANUAL | OTHER` — explicitly marked `PROPOSED_EXTENSION` in
`src/connectors/base.py`'s docstring; the source document never enumerates connector types this
way (it names specific tools — Playwright, Firecrawl — narratively).

## SyntheticFileConnector (Step 3 Section 40)

Reads fixture files from `tests/fixtures/ingestion/`. `discover()` lists filenames (minus
extension) as `source_identifier`s; `fetch()` reads the file, decodes JSON where the extension
suggests it should be JSON, and falls back to raw text on parse failure (never discards malformed
content — see `docs/ingestion/failure-handling.md`).

## ScriptedConnector (test-only auxiliary, `tests/helpers.py`)

Used only where a test needs to control exactly what content is returned across successive
`fetch()` calls for the same identifier (e.g. proving version-chain behavior on changed content).
Not a second production connector — it never leaves the `tests/` tree.

## Source IDs / Requirements

SRC-000009 (scraper concept), SRC-000013 (scraper skeleton). REQ-000009.
