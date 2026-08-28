# Context Migration

Per Step 1 Section 23. Defines conceptual state classes so that a replacement worker never inherits
hallucinated information as trusted knowledge.

## The 10 required state classes

| State class | Definition | Migration rule |
|---|---|---|
| TRUSTED STATE | Data that has passed Verification (per `evidence-model.md`) | Safe to migrate to replacement as-is |
| UNTRUSTED STATE | Raw, unverified worker output (MODEL INFERENCE per `data-lineage.md`) | Migrated but explicitly TAGGED untrusted — replacement must re-derive or re-verify before treating as fact |
| RAW EVIDENCE | Unprocessed evidence artifacts (URLs, hashes, timestamps) | Safe to migrate as-is (it's evidence, not a conclusion) |
| VALIDATED KNOWLEDGE | Same as TRUSTED STATE, using the `data-lineage.md` term for the post-verification record | Safe to migrate |
| MODEL INFERENCE | An LLM judgment not yet verified | **Must NOT be migrated as if it were VALIDATED KNOWLEDGE** — this is the core failure mode this document exists to prevent |
| TASK STATE | What the failing worker was in the middle of doing (current job, queue position) | Migrated to allow the replacement to resume work, not treated as a source of truth about the WORLD |
| CONFIGURATION STATE | The worker's active config version | Migrated as-is (config is not something the worker itself could have hallucinated) |
| MEMORY STATE | RAG/vector-retrieved context the worker was using | Migrated as REFERENCE only — treated like UNTRUSTED STATE if it originated from the worker's own past (possibly hallucinated) outputs |
| CHECKPOINT STATE | A prior known-good save point | Preferred migration source when available (safer than migrating live/failing state) |
| FAILED OUTPUT | The specific output(s) that triggered the Sentinel's quarantine decision | Migrated ONLY to the incident log / admin panel for diagnosis — explicitly NOT migrated to the replacement worker as usable context |

## The core rule

> "A replacement worker must not inherit hallucinated information as trusted knowledge."
> — Step 1 Section 23, restating the concern implicit in SRC-000037's context-transfer requirement.

Concretely: when Context Migration serializes a quarantined worker's state (SRC-000037: "transfer its context
and everything into replacement ai"), the literal instruction ("everything") is NOT followed verbatim by this
architecture — "everything" is explicitly filtered through the state-class table above, with MODEL INFERENCE
and FAILED OUTPUT excluded from the "trusted knowledge" portion of the transfer. **This is a deliberate,
flagged departure from a literal reading of the source's own words**, justified by Step 1 Section 23's
explicit, more specific instruction, which takes precedence as the more recent and more specific governing
directive for this repository. This departure is recorded here rather than silently implemented, per the
no-silent-invention rule.

## Relationship to retirement (non-failure exit)

Per `dynamic-worker-scaling.md`, sub-domain worker RETIREMENT (velocity drop, not a failure) is a DIFFERENT
lifecycle exit than quarantine/Hot-Swap. Retired-worker state does not carry the "possible hallucination"
taint that quarantined-worker state does — a retired worker wasn't necessarily wrong, it just ran out of
volume to justify its own dedicated existence. Its TASK STATE and VALIDATED KNOWLEDGE can be more liberally
preserved/archived for potential reactivation (see `dynamic-worker-scaling.md`'s "Worker reactivation" gap)
without the same UNTRUSTED-STATE filtering quarantine requires.

## Source basis and status

The 10-state-class taxonomy itself is `PROPOSED_EXTENSION` (the source never itemizes these distinctly) —
required directly by Step 1 Section 23's explicit instruction to "Define conceptual state classes." Every
individual state class listed traces to a real source concept (task state, config, memory/RAG, checkpoints,
failed output) even though the source never organizes them into this taxonomy itself.
