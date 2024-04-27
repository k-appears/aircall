import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, ContextManager, Optional


@dataclass
class EventOutcome(ABC):
    """Represents Alert, Acknowledge and ACK Timeout events."""

    source_event_id: str
    alert_id: str
    monitored_service_id: str
    timestamp: float = time.time()


@dataclass
class AlertEventOutcome(EventOutcome):
    message: str = "Alerting Service has detected an issue"
    timestamp: float = time.time()


@dataclass
class AcknowledgeEventOutcome(EventOutcome):
    timestamp: float = time.time()


@dataclass
class AckTimeoutEventOutcome(EventOutcome):
    timestamp: float = time.time()


@dataclass
class HealthyEventOutcome(EventOutcome):
    timestamp: float = time.time()


class StatusOutcome(Enum):
    HEALTHY = 1
    UNHEALTHY = 2


@dataclass
class StatusEventOutcome:
    status: StatusOutcome
    monitored_service_id: str
    source_event_id: str = "Initialisation Event"
    timestamp: float = time.time()


class SaveEventError(Exception):
    pass


class PersistencyOutcomePort(ABC):
    @abstractmethod
    def save_event(self, alert_event: EventOutcome) -> None:
        pass

    @abstractmethod
    def get_events_by_alert_id(self, alert_id: str) -> list[EventOutcome]:
        pass

    @abstractmethod
    def save_status_event(self, status_event: StatusEventOutcome) -> None:
        pass

    @abstractmethod
    def get_last_status_event(self, alert_id: str) -> Optional[StatusEventOutcome]:
        pass

    @abstractmethod
    def save_notification_event(self, level_idx: int, message: str, recipient: str, channel: str) -> None:
        pass

    @abstractmethod
    def get_last_notification_level_index(self, alert_id: str) -> int:
        pass

    @abstractmethod
    def start_transaction(self) -> ContextManager[Any]:
        pass

    @abstractmethod
    def rollback_transaction(self) -> None:
        pass
