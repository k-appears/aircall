from abc import ABC, abstractmethod


class NotificationOutcomeAdapter(ABC):
    @abstractmethod
    def send_notification(self, message: str, recipient: str, channel: str) -> None:
        pass


class EmailOutcomeAdapter(NotificationOutcomeAdapter):
    def send_notification(self, message: str, recipient: str, channel: str) -> None:
        pass


class SMSOutcomeAdapter(NotificationOutcomeAdapter):
    def send_notification(self, message: str, recipient: str, channel: str) -> None:
        pass
