from abc import abstractmethod
from typing import Any, ContextManager

from app.ports.outcoming.persistency import (
    EventOutcome,
    PersistencyOutcomePort,
    StatusEventOutcome,
)


class PersistencyOutcomeAdapter(PersistencyOutcomePort):
    @abstractmethod
    def get_last_notification_level_index(self, alert_id: str) -> int:
        pass

    @abstractmethod
    def get_last_status_event(self, alert_id: str) -> StatusEventOutcome:
        pass

    @abstractmethod
    def save_status_event(self, status_event: StatusEventOutcome) -> None:
        pass

    @abstractmethod
    def get_events_by_alert_id(self, alert_id: str) -> list[EventOutcome]:
        pass

    @abstractmethod
    def save_event(self, alert_event: EventOutcome) -> None:
        pass

    @abstractmethod
    def save_notification_event(self, level_idx: int, message: str, recipient: str, channel: str) -> None:
        pass

    @abstractmethod
    def start_transaction(self) -> ContextManager[Any]:
        pass

    @abstractmethod
    def rollback_transaction(self) -> None:
        pass
