"""
Health check registry. Per Step 3 Section 51: health checks for source registry, storage,
ingestion engine, connector registry, event system, quarantine, raw retrieval -- each must
distinguish HEALTHY / DEGRADED / UNHEALTHY / UNKNOWN.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable, Optional


class HealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class HealthResult:
    component: str
    status: HealthStatus
    detail: str
    checked_at: str


class HealthRegistry:
    """A component registers a zero-arg callable returning HealthResult; the registry aggregates."""

    def __init__(self):
        self._checks: dict[str, Callable[[], HealthResult]] = {}

    def register(self, component: str, check_fn: Callable[[], HealthResult]) -> None:
        self._checks[component] = check_fn

    def check(self, component: str) -> HealthResult:
        fn = self._checks.get(component)
        if fn is None:
            return HealthResult(
                component=component,
                status=HealthStatus.UNKNOWN,
                detail="no health check registered for this component",
                checked_at=datetime.now(timezone.utc).isoformat(),
            )
        try:
            return fn()
        except Exception as exc:  # a failing health check itself is UNHEALTHY, never silently HEALTHY
            return HealthResult(
                component=component,
                status=HealthStatus.UNHEALTHY,
                detail=f"health check raised: {exc}",
                checked_at=datetime.now(timezone.utc).isoformat(),
            )

    def check_all(self) -> dict[str, HealthResult]:
        return {name: self.check(name) for name in self._checks}


def simple_health(component: str, status: HealthStatus, detail: str = "") -> HealthResult:
    return HealthResult(component=component, status=status, detail=detail, checked_at=datetime.now(timezone.utc).isoformat())
