"""
Configuration seed values. Per docs/contracts/configuration.md (Step 2) and
docs/audit/threshold-preservation-audit.md (Step 3): exactly 7 System-A configuration thresholds,
preserved with their EXACT source-derived values. THRESH-003 (Explore/Exploit split) is recorded
for interface-completeness even though System B owns its execution.

Do NOT modify these values. If a real value needs tuning later, that is a new CONFIG-V(n+1) row
via SourceRegistry-style versioning (docs/database/versioning.md), never an edit of this seed data.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConfigurationSeed:
    scope: str
    value: Any
    source_threshold_id: str
    description: str


CONFIGURATION_SEEDS: list[ConfigurationSeed] = [
    ConfigurationSeed(
        scope="worker.spawn_threshold",
        value=5,
        source_threshold_id="THRESH-001",
        description="Sub-domain worker spawn trigger: >5 leads/day (the '5-Lead Rule')",
    ),
    ConfigurationSeed(
        scope="worker.retire_threshold",
        value={"value": 2, "window_days": 7},
        source_threshold_id="THRESH-002",
        description="Sub-domain worker retirement trigger: <2 leads/day, 7-day rolling average",
    ),
    ConfigurationSeed(
        scope="strategist.explore_exploit_split",
        value={"exploit": 80, "explore": 20},
        source_threshold_id="THRESH-003",
        description="Strategist strategy-selection policy (System B, referenced for interface-completeness)",
    ),
    ConfigurationSeed(
        scope="sentinel.drift_threshold",
        value=0.85,
        source_threshold_id="THRESH-004",
        description="Sentinel drift-score hot-swap trigger: D_t >= 0.85",
    ),
    ConfigurationSeed(
        scope="sentinel.consecutive_failure_threshold",
        value=3,
        source_threshold_id="THRESH-005",
        description="Sentinel discrete failure-count hot-swap trigger: >=3 consecutive schema/validation errors",
    ),
    ConfigurationSeed(
        scope="saturation.threshold",
        value={"consistency_percent": 99.5, "window_hours": 72},
        source_threshold_id="THRESH-006",
        description="Metric Evolution saturation-idle trigger",
    ),
    ConfigurationSeed(
        scope="triage.budget_sanity_filter",
        value={"enabled": True, "rule": "reject listings whose stated unit price makes the stated volume mathematically uneconomical"},
        source_threshold_id="THRESH-015",
        description="Deterministic Triage (Layer 0) Budget Sanity Filter -- newly registered as a configuration value in Step 3 (see docs/audit/threshold-preservation-audit.md)",
    ),
]


def seed_map() -> dict[str, ConfigurationSeed]:
    return {c.scope: c for c in CONFIGURATION_SEEDS}
