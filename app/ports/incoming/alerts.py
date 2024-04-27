from abc import ABC, abstractmethod

from app.domain.entities.alert import Alert


class AlertingIncomingPort(ABC):
    @abstractmethod
    def receives_alert(self, alert: Alert) -> None:
        pass
