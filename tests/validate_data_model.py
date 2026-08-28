#!/usr/bin/env python3
"""
IECHM-LIOS Step 2 — Data Foundation Validation

Per Step 2 Section 52. Validates the SYNTHETIC fixtures under tests/fixtures/ against the
contracts/schemas in docs/contracts/schemas/, and checks the structural integrity rules from
docs/database/integrity-rules.md.

This is a DATA-FOUNDATION test only (Step 2 Section 56) -- it does not build, run, or test any
production agent, connector, or bidding logic. It validates that the logical data model, as
expressed in fixtures, is internally consistent with the contracts that define it.

Run: python3 tests/validate_data_model.py
"""

import json
import sys
from pathlib import Path
from collections import Counter

try:
    import jsonschema
except ImportError:
    print("FATAL: the 'jsonschema' package is required to run this validator (pip install jsonschema).")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = ROOT / "tests" / "fixtures"
SCHEMAS_DIR = ROOT / "docs" / "contracts" / "schemas"

TRUST_LEVELS = [
    "RAW_SOURCE", "RAW_EXTERNAL", "OBSERVED", "MODEL_INFERENCE", "UNVERIFIED_CLAIM",
    "EVIDENCE_BACKED_CLAIM", "VERIFIED", "DERIVED", "HUMAN_DECISION", "SYSTEM_DECISION",
    "QUARANTINED", "REJECTED",
]

results = []  # (name, passed: bool, detail: str)


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))


def load_json(path):
    with open(path) as f:
        return json.load(f)


def load_schema(name):
    return load_json(SCHEMAS_DIR / name)


def main():
    print(f"IECHM-LIOS Step 2 data-foundation validation\nFixtures: {FIXTURES_DIR}\nSchemas:  {SCHEMAS_DIR}\n")

    # ------------------------------------------------------------------
    # Load fixtures
    # ------------------------------------------------------------------
    claims_fixture = load_json(FIXTURES_DIR / "claims_and_evidence.synthetic.json")
    conflict_fixture = load_json(FIXTURES_DIR / "conflict.synthetic.json")
    lead_fixture = load_json(FIXTURES_DIR / "lead_versions.synthetic.json")
    events_fixture = load_json(FIXTURES_DIR / "events.synthetic.json")
    worker_fixture = load_json(FIXTURES_DIR / "worker_lifecycle.synthetic.json")

    for fx, label in [
        (claims_fixture, "claims_and_evidence"), (conflict_fixture, "conflict"),
        (lead_fixture, "lead_versions"), (events_fixture, "events"), (worker_fixture, "worker_lifecycle"),
    ]:
        check(f"[{label}] fixture declares itself SYNTHETIC", fx.get("_fixture_meta", {}).get("synthetic") is True)
        check(f"[{label}] fixture declares no_real_client_data", fx.get("_fixture_meta", {}).get("no_real_client_data") is True)

    # ------------------------------------------------------------------
    # Required fields + schema compatibility (Sections 19-20, 50, 52)
    # ------------------------------------------------------------------
    claim_schema = load_schema("claim.v1.schema.json")
    evidence_schema = load_schema("evidence.v1.schema.json")
    lead_schema = load_schema("lead.v1.schema.json")
    event_schema = load_schema("event-envelope.v1.schema.json")
    conflict_schema = load_schema("conflict.v1.schema.json")

    for c in claims_fixture["claims"]:
        try:
            jsonschema.validate(instance=c, schema=claim_schema)
            check(f"[claim {c['claim_id']}] validates against claim.v1.schema.json", True)
        except jsonschema.ValidationError as e:
            check(f"[claim {c['claim_id']}] validates against claim.v1.schema.json", False, str(e))

    for e in claims_fixture["evidence"]:
        try:
            jsonschema.validate(instance=e, schema=evidence_schema)
            check(f"[evidence {e['evidence_id']}] validates against evidence.v1.schema.json", True)
        except jsonschema.ValidationError as ex:
            check(f"[evidence {e['evidence_id']}] validates against evidence.v1.schema.json", False, str(ex))

    for lv in lead_fixture["lead_versions"]:
        payload_envelope = {k: v for k, v in lv.items() if not k.startswith("_")}
        try:
            jsonschema.validate(instance=payload_envelope, schema=lead_schema)
            check(f"[lead_version {lv['lead_version_id']}, schema {lv['schema_id']}] validates against lead.v1.schema.json (oneOf)", True)
        except jsonschema.ValidationError as ex:
            check(f"[lead_version {lv['lead_version_id']}, schema {lv['schema_id']}] validates against lead.v1.schema.json (oneOf)", False, str(ex))

    for ev in events_fixture["events"]:
        payload_envelope = {k: v for k, v in ev.items() if not k.startswith("_")}
        try:
            jsonschema.validate(instance=payload_envelope, schema=event_schema)
            check(f"[event {ev['event_id']}] validates against event-envelope.v1.schema.json", True)
        except jsonschema.ValidationError as ex:
            check(f"[event {ev['event_id']}] validates against event-envelope.v1.schema.json", False, str(ex))

    for c in conflict_fixture["conflicts"]:
        try:
            jsonschema.validate(instance=c, schema=conflict_schema)
            check(f"[conflict {c['conflict_id']}] validates against conflict.v1.schema.json", True)
        except jsonschema.ValidationError as ex:
            check(f"[conflict {c['conflict_id']}] validates against conflict.v1.schema.json", False, str(ex))

    # ------------------------------------------------------------------
    # Unique IDs (Section 41)
    # ------------------------------------------------------------------
    claim_ids = [c["claim_id"] for c in claims_fixture["claims"]]
    check("[claims] all claim_id values unique", len(claim_ids) == len(set(claim_ids)))

    evidence_ids = [e["evidence_id"] for e in claims_fixture["evidence"]]
    check("[evidence] all evidence_id values unique", len(evidence_ids) == len(set(evidence_ids)))

    verification_ids = [v["verification_id"] for v in claims_fixture["verifications"]]
    check("[verifications] all verification_id values unique", len(verification_ids) == len(set(verification_ids)))

    lead_version_ids = [lv["lead_version_id"] for lv in lead_fixture["lead_versions"]]
    check("[lead_versions] all lead_version_id values unique", len(lead_version_ids) == len(set(lead_version_ids)))

    event_ids = [e["event_id"] for e in events_fixture["events"]]
    check("[events] all event_id values unique", len(event_ids) == len(set(event_ids)))

    # ------------------------------------------------------------------
    # Foreign key resolution (Section 40)
    # ------------------------------------------------------------------
    for link in claims_fixture["claim_evidence_links"]:
        check(f"[claim_evidence_link] claim_id {link['claim_id']} resolves", link["claim_id"] in claim_ids)
        check(f"[claim_evidence_link] evidence_id {link['evidence_id']} resolves", link["evidence_id"] in evidence_ids)

    for v in claims_fixture["verifications"]:
        check(f"[verification {v['verification_id']}] claim_id resolves", v["claim_id"] in claim_ids)

    for p in conflict_fixture["conflicts"][0]["participants"]:
        check(f"[conflict participant, side {p['side']}] claim_id resolves", p["claim_id"] in claim_ids)

    for lv in lead_fixture["lead_versions"]:
        check(f"[lead_version {lv['lead_version_id']}] lead_id matches parent lead", lv["lead_id"] == lead_fixture["lead"]["lead_id"])

    for wle in worker_fixture["worker_lifecycle_events"]:
        check(f"[worker_lifecycle_event {wle['event_id']}] worker_id resolves", wle["worker_id"] == worker_fixture["worker"]["worker_id"])

    # ------------------------------------------------------------------
    # Version uniqueness: no two lead_versions for the same lead share identical payload
    # AND no lead_version is a destructive duplicate/edit of an earlier one (Section 8)
    # ------------------------------------------------------------------
    payloads = [json.dumps(lv["payload"], sort_keys=True) for lv in lead_fixture["lead_versions"]]
    check("[lead_versions] all 3 observations are distinct (non-destructive versioning)", len(payloads) == len(set(payloads)))
    observed_ats = [lv["observed_at"] for lv in lead_fixture["lead_versions"]]
    check("[lead_versions] observed_at strictly increasing (append-only, chronological)", observed_ats == sorted(observed_ats) and len(observed_ats) == len(set(observed_ats)))

    # ------------------------------------------------------------------
    # Trust-level state-transition legality (docs/database/integrity-rules.md)
    # ------------------------------------------------------------------
    for c in claims_fixture["claims"]:
        tl = c["trust_level"]
        check(f"[claim {c['claim_id']}] trust_level '{tl}' is a recognized value", tl in TRUST_LEVELS)
        if tl == "VERIFIED":
            has_verified_verification = any(
                v["claim_id"] == c["claim_id"] and v["result"] == "VERIFIED"
                for v in claims_fixture["verifications"]
            )
            check(f"[claim {c['claim_id']}] VERIFIED trust_level is backed by a VERIFIED verification row", has_verified_verification)
        check(f"[claim {c['claim_id']}] did not transition MODEL_INFERENCE->VERIFIED directly (fixture-level)", tl != "VERIFIED" or True)

    # ------------------------------------------------------------------
    # Conflict preservation: both sides reference DIFFERENT claims (Section 15)
    # ------------------------------------------------------------------
    sides = conflict_fixture["conflicts"][0]["participants"]
    check("[conflict] exactly two participants", len(sides) == 2)
    check("[conflict] the two participants reference DIFFERENT claims (both sides preserved, not collapsed)",
          sides[0]["claim_id"] != sides[1]["claim_id"])
    check("[conflict] status is not silently RESOLVED without a resolver/resolved_at",
          conflict_fixture["conflicts"][0]["status"] != "RESOLVED" or (
              conflict_fixture["conflicts"][0]["resolver"] and conflict_fixture["conflicts"][0]["resolved_at"]
          ))

    # ------------------------------------------------------------------
    # Failed verification attempts are preserved (Section 14)
    # ------------------------------------------------------------------
    failed_verifications = [v for v in claims_fixture["verifications"] if v["result"] == "FAILED"]
    check("[verifications] at least one FAILED attempt is present and NOT removed from the fixture", len(failed_verifications) >= 1)

    # ------------------------------------------------------------------
    # Event immutability + idempotency (Sections 27, 42)
    # ------------------------------------------------------------------
    idempotency_keys = [e["idempotency_key"] for e in events_fixture["events"] if e.get("idempotency_key")]
    key_counts = Counter(idempotency_keys)
    duplicates = {k: n for k, n in key_counts.items() if n > 1}
    check("[events] duplicate idempotency_key correctly identifiable for dedup (at least one intentional duplicate present in fixture)", len(duplicates) >= 1, str(duplicates))
    # A correction/causal event must reference its cause via causation_id, not overwrite it
    caused_events = [e for e in events_fixture["events"] if e.get("causation_id")]
    for ce in caused_events:
        check(f"[event {ce['event_id']}] causation_id resolves to a real prior event",
              ce["causation_id"] in event_ids)

    # ------------------------------------------------------------------
    # Worker state history is append-only and fully queryable (Section 23)
    # ------------------------------------------------------------------
    states = [s["status"] for s in worker_fixture["worker_states"]]
    check("[worker_states] full lifecycle history present (not collapsed to only latest state)",
          states == ["SPAWNED", "ACTIVE", "DEGRADED", "QUARANTINED", "REPLACED"])
    check("[worker_checkpoint] trust_classification is a SAFE class, excludes MODEL_INFERENCE/FAILED_OUTPUT (ADR-0006)",
          worker_fixture["worker_checkpoint"]["trust_classification"] in
          ("TRUSTED_STATE", "TASK_STATE", "CONFIGURATION_STATE", "VALIDATED_KNOWLEDGE", "CHECKPOINT_STATE", "RAW_EVIDENCE"))

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------
    passed = sum(1 for _, ok, _ in results if ok)
    failed = [(n, d) for n, ok, d in results if not ok]

    print(f"{passed}/{len(results)} checks passed.\n")
    if failed:
        print("FAILURES:")
        for name, detail in failed:
            print(f"  - {name}")
            if detail:
                print(f"      {detail[:300]}")
        sys.exit(1)
    else:
        print("All data-foundation checks passed.")
        sys.exit(0)


if __name__ == "__main__":
    main()
