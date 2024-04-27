from abc import ABC, abstractmethod

from app.domain.entities.events import AckTimeoutIncomeEvent


class TimerServiceIncomingPort(ABC):
    @abstractmethod
    def receives_acknowledge_timeout(self, ack_event: AckTimeoutIncomeEvent) -> None:
        pass
