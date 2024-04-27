from app.adapters.outcoming.notification import EmailOutcomeAdapter, SMSOutcomeAdapter
from app.domain.value_objects.policy import (
    EmailTargetPolicy,
    SMSTargetPolicy,
    TargetPolicy,
)


class NotificationOutcomePort:
    def __init__(self) -> None:
        self.strategy_mapping = {
            SMSTargetPolicy: SMSOutcomeAdapter(),
            EmailTargetPolicy: EmailOutcomeAdapter(),
        }

    def __call__(self, target: TargetPolicy, message: str) -> None:
        try:
            strategy_instance = self.strategy_mapping[type(target)]
        except KeyError:
            raise ValueError(f"Key '{target}' not found as notification")

        strategy_instance.send_notification(
            message=message,
            recipient=target.recipient,
            channel=target.__class__.__name__,
        )
