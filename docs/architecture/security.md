# Security Architecture

Per Step 1 Section 30. Treats all external content as untrusted. Preserves source security concepts; new
security architecture is marked `PROPOSED_EXTENSION`, never presented as a source requirement.

## Source-preserved security concepts

| Concept | Source | Applies to IECHM-LIOS how |
|---|---|---|
| Prompt injection | SRC-000001, SRC-000030 | The source's Sanitizer is a System B concept, but the underlying THREAT (a scraped listing containing text designed to manipulate an LLM classifier) applies equally to System A's own Layer 1 classification agents — see `subsystems.md` #6 (Security/Sanitization, recon-data variant), which is `INTERPRETATION`, not `DIRECT_MAPPING`, precisely because the source never explicitly extends this defense to System A |
| Malicious content | SRC-000030 | Same as above |
| Sanitization | SRC-000001, SRC-000030 | Same as above |
| Credential leakage | Not named explicitly by source | `PROPOSED_EXTENSION` — necessary given External Integration (`subsystems.md` #30) requires credentials for authenticated platform access |
| Unsafe URLs | Implied by URL verification (SRC-000039) needing to fetch untrusted URLs safely | `PROPOSED_EXTENSION` for the SANDBOXING requirement specifically (source names the verification ACTION, not its safety precautions) |
| Tool abuse | Not named explicitly | `PROPOSED_EXTENSION` — relevant once any agent has tool-calling capability (e.g., a Platform Worker's scraper connector) |
| Agent permissions | Implied by Agent Control Plane's need for scoped access (`agent-control-plane.md`) | `PROPOSED_EXTENSION` as a formal permission MODEL; individual permission NEEDS are `SOURCE-DERIVED` (e.g., "read-only external access to its platform" per `agent-topology.md`) |
| Configuration protection | Implied by Configuration versioning/audit needs (`configuration.md`) | `PROPOSED_EXTENSION` |
| Memory poisoning | Not named explicitly, but the RAG/Strategy-Ledger trust concern (`memory.md`) implies it | `PROPOSED_EXTENSION` |
| Evidence poisoning | Not named explicitly | `PROPOSED_EXTENSION` — an adversarial lead source could supply fabricated "evidence" (e.g., a fake but resolvable URL) designed to pass Verification; this is a genuine gap the Evidence Model (`evidence-model.md`) does not fully close on its own |
| Runaway agents | Implied by the entire Sentinel/Hot-Swap design existing at all (`sentinel-plane.md`) | `SOURCE-DERIVED` as a MOTIVATING concern; the specific term "runaway agents" is this document's own framing |
| Runaway cost | Implied by Layer 0's entire rationale ("you cannot send all of them to an LLM... this would cost tens of thousands of dollars a day," SRC-000053) | `SOURCE-DERIVED` as a motivating concern; formal cost LIMITS as an enforcement mechanism are `PROPOSED_EXTENSION` (`agent-control-plane.md`, `subsystems.md` #26) |
| Rate limits | SRC-000001 ("API/rate limits" as data to extract per-platform) | `SOURCE-DERIVED` as DATA TO TRACK about external platforms; IECHM-LIOS's OWN outbound rate-limiting discipline (to avoid triggering platform bans while scraping) is `PROPOSED_EXTENSION` |

## Treat all external content as untrusted — the governing principle

Per Step 1 Section 30's opening instruction, every scraped listing, RFQ, forum post, or crowdfunding page
IECHM-LIOS ingests is untrusted input, full stop — regardless of which platform it came from. This principle
governs: Raw Payload Storage (never executed/rendered, only stored as data — `subsystems.md` #4); Security/
Sanitization (#6); Evidence artifacts (stored HTML snapshots must not be unsafely rendered — `evidence-model.md`);
and Memory (retrieved RAG content is still untrusted until independently verified — `memory.md`).

## No unsupported security claims presented as source requirements

Every `PROPOSED_EXTENSION` item above is explicitly labeled as such. None is presented as if the source PDF
specified it. The source PDF is a brainstorming transcript about business/agent architecture, not a security
review — most of the concrete security engineering (credential isolation, sandboxing, rate-limiting
discipline, permission models) is necessarily `PROPOSED_EXTENSION`, filling gaps the source leaves entirely
open, per Step 1 Section 30's explicit allowance for this.

## Explicit non-implementation

No security controls are implemented in Step 1 (Section 42). A future dedicated security-review pass (the
`security-review` skill referenced in this session's tooling) would be the appropriate place to harden this
further once real code exists.
