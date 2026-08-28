# Quarantine

Per Step 3 Sections 18-19. Implementation: `src/quarantine/store.py`, `src/security/inspector.py`.

## Routing logic (Step 3 Section 18)

```
RAW INPUT -> SECURITY INSPECTION -> SAFE | SUSPICIOUS | MALICIOUS | UNKNOWN -> PROCESS or QUARANTINE
```

Implemented routing decision (`src/ingestion/engine.py::QUARANTINE_VERDICTS`):
`SUSPICIOUS` and `MALICIOUS` -> **QUARANTINE**. `SAFE` and `UNKNOWN` -> **PROCESS**.

This is a deliberate, documented choice: `UNKNOWN` means "the deterministic inspector found no
recognized pattern," which is not evidence of a threat (over-quarantining everything ambiguous
would defeat the purpose of having graduated severity levels at all) — it proceeds to normal
processing. `SUSPICIOUS` is treated as cautiously as `MALICIOUS` (both quarantine) because Step 3
Section 20's trust boundary is non-negotiable: any detected injection-style pattern, even a "soft"
one (e.g. "you are now..."), is routed away from unmediated processing.

## Quarantine record retention (Step 3 Section 19)

`QuarantineStore` never deletes a `QuarantineRecord`. `release()` performs a STATUS TRANSITION
(`QUARANTINED -> RELEASED` or `-> CONFIRMED_MALICIOUS`), setting `released_at`/`release_actor`/
`release_reason` — the record itself, including its original `reason`/`detection_type`/`severity`,
is permanent.

## The quarantined raw record itself is also never deleted

Quarantine only prevents an Observation from being created (the pipeline stops after
`RawRecordQuarantined` is emitted) — the `RawRecord` was already stored BEFORE security inspection
runs, so quarantined content remains fully queryable raw data, per the Absolute Rule.

## Source IDs / Requirements

SRC-000001 (Sanitizer concept, generalized here for the recon-side ingestion layer per
`docs/architecture/subsystems.md` #6's `INTERPRETATION` status), SRC-000039. REQ-000019, REQ-000030.
