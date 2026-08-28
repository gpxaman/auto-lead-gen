# Contract: Task

**Version:** v0.1-DRAFT | **Status:** DRAFT, not implemented, not approved

## Purpose
What an agent instance is/was doing. Failed attempts are preserved, never erased by a successful retry.

## Source references
Implied by Task State (`docs/architecture/context-migration.md`), no direct source schema.

## Requirement references
REQ-000018.

## Fields

### `task`
`task_id`, `agent_instance_id`, `task_type`, `input_reference`, `created_at`.

### `task_attempt` (append-only)
| Field | Required? | Tag | Notes |
|---|---|---|---|
| `task_attempt_id` | required | `PROPOSED_SCHEMA` | |
| `task_id` | required | `PROPOSED_SCHEMA` | |
| `attempt_number` | required | `PROPOSED_SCHEMA` | monotonic per task |
| `status` | required | `PROPOSED_SCHEMA` | `SUCCESS` \| `FAILED` \| `IN_PROGRESS` |
| `output_reference` | optional | `PROPOSED_SCHEMA` | |
| `error` | optional | `PROPOSED_SCHEMA` | populated when `status = FAILED` |
| `started_at` / `completed_at` | required/optional | `PROPOSED_SCHEMA` | |
| `configuration_version_id`, `model_version_id`, `prompt_version_id` | optional | `DERIVED_CANONICAL_SCHEMA` | provenance |
| `checkpoint_reference` | optional | `PROPOSED_SCHEMA` | ties to `worker_checkpoint` |

### `task_result`
`task_attempt_id`, `result_data`, `claim_ids[]` (if the task produced claims).

### `task_error`
`task_attempt_id`, `error_type`, `error_message`, `stack_reference` (nullable).

### `task_checkpoint`
`task_id`, `checkpoint_data`, `created_at`.

## Validation rules
**"A successful retry must not erase the failed attempt"** (Step 2 Section 22, explicit) — enforced by
`task_attempt` being append-only/insert-only, `(task_id, attempt_number)` unique, never updated in place
except transitioning `IN_PROGRESS → SUCCESS/FAILED` once.

## Provenance
Full field set per `docs/database/provenance.md` — `task_attempt` is itself one of the primary provenance
ANCHORS other records point back to (`claim.task_id`, etc.).

## Versioning & compatibility
N/A — tasks are inherently instance data, not a versioned definition.

## Security classification
`INTERNAL`.

## Examples
None — no source example exists for this `PROPOSED_EXTENSION` entity.
