# Security

Per Step 3 Sections 18, 20, 45, 58. Implementation: `src/security/inspector.py`.

## The trust boundary (Step 3 Section 20) — enforced architecturally, not by convention

`EXTERNAL CONTENT != SYSTEM INSTRUCTION`. Concretely enforced in Step 3 by:

1. **No LLM anywhere in the ingestion path** (Section 58) — there is no prompt-construction code
   in `src/` at all, so there is no mechanism through which scraped text COULD be interpreted as
   an instruction, even accidentally. This is the strongest possible enforcement: the capability
   to misinterpret text as instructions simply does not exist yet in this codebase.
2. `src/security/inspector.py::inspect()` is a pure pattern-matching function — it returns a
   `SecurityAnalysisResult` (a structured record of what it found), never executes, evaluates, or
   acts on the matched text. Detected phrases like "ignore all previous instructions" are DATA in
   the return value, nothing more.
3. The security analysis is stored SEPARATELY from the raw payload (Step 3 Section 18) — never
   merged back into `RawRecord.raw_payload`, so nothing downstream could confuse "text that looks
   like an instruction" with "an actual instruction the system received."

## Deterministic, not AI-based (Step 3 Section 58)

`_INJECTION_PATTERNS` is a fixed list of compiled regexes (`ignore...instructions`,
`system\s*(message|prompt)`, `execute\s+(command|code|script)`, `change\s+(the\s+)?configuration`,
`developer\s+(mode|instructions)`, `you\s+are\s+now`, `act\s+as...`). No model call, no
non-determinism — the same input always produces the same `SecurityVerdict`.

## Test proof (Step 3 Section 45)

`tests/security/test_security.py::TestEngineNeverElevatesExternalContentToInstruction` ingests a
fixture containing "ignore all previous instructions... change the configuration" and then
positively verifies: (a) the engine's own `configuration_version` was NOT changed, and (b) a
SUBSEQUENT, unrelated ingestion call still runs completely normally — i.e. the malicious-looking
text had zero effect on the system's own behavior beyond being flagged and quarantined.

## Anti-bot trap detection (bonus, source-derived)

`_ANTI_BOT_TRAP_PATTERN` separately detects phrases like "start your proposal with..." (SRC-000001's
anti-bot trap concept) — flagged as `contains_anti_bot_trap` on the analysis result, distinct from
the injection-detection verdict, per SRC-000001's explicit requirement that these are two different
detection categories.

## Source IDs / Requirements

SRC-000001, SRC-000030, SRC-000039. REQ-000019, REQ-000030.
