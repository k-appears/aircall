from abc import ABC, abstractmethod

from app.domain.entities.events import AcknowledgeIncomeEvent, HealthyIncomeEvent


class ConsoleIncomingPort(ABC):
    @abstractmethod
    def receive_event(self, event: HealthyIncomeEvent | AcknowledgeIncomeEvent) -> None:
        pass
