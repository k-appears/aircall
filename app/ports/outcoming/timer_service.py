from abc import ABC, abstractmethod


class TimerServiceOutcomePort(ABC):
    @abstractmethod
    def set_timer(self, service_id: str, delay: int) -> None:
        pass
