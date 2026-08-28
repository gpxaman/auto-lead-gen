# Dynamic Worker Scaling

Per Step 1 Section 20. Preserves the source's dynamic sub-domain worker concept and its EXACT numerical
thresholds, treated as source-defined policy/defaults, not universal production truth, and not silently
changed.

## Source-defined thresholds (preserved exactly)

| Parameter | Value | Source |
|---|---|---|
| Worker spawn threshold | > 5 leads/day (sustained, for a given sub-domain) | THRESH-001, SRC-000036 ("the 5-Lead Rule") |
| Worker retirement threshold | < 2 leads/day, measured as a 7-day trailing/rolling average | THRESH-002, SRC-000036 |

These two numbers (5 and 2, and the 7-day averaging window) are the ONLY numeric scaling parameters the
source provides. Every other field below is either a necessary operational detail the source implies but
doesn't quantify, or an explicit gap.

## Lead velocity / rolling averages

Source basis: "over a 7-day trailing average" (spawn context is less explicit — the source states the >5/day
spawn condition without specifying whether it must be sustained over any window, or a single day's count is
sufficient). **This is an ambiguity, not resolved by inventing an answer:** SRC-000036/THRESH-001 says "If any
specific sub-domain... reaches an int[...]" (truncated in source) — the exact intake-measurement window for
the SPAWN condition specifically is `SOURCE_INCOMPLETE` (the source's own sentence describing it is cut off
mid-word). Only the RETIREMENT condition's 7-day window is fully stated. This gap is preserved, not filled in
with an assumed matching 7-day window for spawn.

## Worker spawn threshold, retirement threshold — see table above.

## Worker cooldown
Not specified by the source at all. `PROPOSED_EXTENSION` — needed to prevent a sub-domain hovering near the
5-lead boundary from rapidly spawning and retiring (thrashing). No default value is proposed here (that would
be inventing a number); this is flagged purely as an architectural gap requiring a Step 2+ decision.

## Spawn protection
Not specified. `PROPOSED_EXTENSION` — a mechanism to prevent spawning a duplicate worker for a sub-domain that
already has one active (race condition if two velocity-check cycles overlap). Flagged as a gap only.

## Duplicate-worker prevention
Same as above — `PROPOSED_EXTENSION`, gap only, no invented mechanism.

## Maximum workers
Not specified by the source as an explicit cap. The only related figures are the AGGREGATE agent-count
ESTIMATES (140-195 total, TABLE-004) which are illustrative sizing projections, not stated as hard caps.
Whether a maximum-worker CAP should exist (vs. letting the 5-Lead Rule alone bound growth organically) is
`NEEDS_USER_DECISION` — seeAI `open-decisions.md`.

## Resource limits
Not specified. `PROPOSED_EXTENSION`, tied to Cost Management (`subsystems.md` #26) and the token/spawn limits
gap already flagged in `agent-control-plane.md`.

## State migration
Covered separately and in full in `docs/architecture/context-migration.md` — applies to BOTH the spawn path
(a new worker inheriting parent Tier 3 persona/compliance parsers, SRC-000036: "inherits the specialized
persona, sub-domain terminology, specific compliance constraints") and the retirement path (state "safely
drained, serialized").

## Worker retirement
Source-derived (SRC-000036, THRESH-002) — "the sub-agent is deprecated or merged back in[to the parent]" —
note the sentence is truncated ("merged back in[to]"), so the EXACT mechanics of "merging back into the
parent" (does the parent Tier 3 worker absorb the retired sub-domain's future monitoring responsibility? Is
this automatic or does it require the sub-domain to be re-discovered later?) are `SOURCE_INCOMPLETE`.

## Worker reactivation
Not explicitly addressed. If a retired sub-domain's lead velocity rises again above 5/day, does it get a
fresh spawn (new agent, no memory of prior operation) or does the archived/serialized state from its prior
active period get restored? The source doesn't say. `UNRESOLVED` — flagged rather than assumed either way,
since this materially affects whether Context Migration's archive step needs long-term retention.

## Explicit summary of what is genuinely source-defined vs. genuinely a gap

| Item | Status |
|---|---|
| Spawn threshold value (5/day) | `SOURCE-DERIVED` |
| Retirement threshold value (2/day, 7-day avg) | `SOURCE-DERIVED` |
| Spawn measurement window | `SOURCE_INCOMPLETE` (sentence truncated in source) |
| New worker inherits parent persona/parsers | `SOURCE-DERIVED` |
| Retirement = "merged back into parent," exact mechanics | `SOURCE_INCOMPLETE` |
| Cooldown, spawn protection, duplicate prevention, max workers, resource limits, reactivation semantics | `PROPOSED_EXTENSION` or `UNRESOLVED` gaps, none filled in with invented numbers |
