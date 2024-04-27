from app.domain.entities.alert import Alert
from app.ports.outcoming.escalation_policy import EscalationPolicyOutcomePort
from app.ports.outcoming.notification import NotificationOutcomePort
from app.ports.outcoming.persistency import (
    AlertEventOutcome,
    PersistencyOutcomePort,
    SaveEventError,
    StatusEventOutcome,
    StatusOutcome,
)
from app.ports.outcoming.timer_service import TimerServiceOutcomePort


class AlertService:
    """
    It is responsible for handling alerts

    On Alert Received:
        Check if Monitored Service is Healthy.
        If yes, set to Unhealthy, notify first level targets, and set timeout.
        If no, ignore if it's already Unhealthy.
    """

    def __init__(
        self,
        escalation_policy: EscalationPolicyOutcomePort,
        persistence: PersistencyOutcomePort,
        timer_service: TimerServiceOutcomePort,
        notification: NotificationOutcomePort,
    ):
        self._escalation_policy = escalation_policy
        self._timer_service = timer_service
        self._persistence = persistence
        self._notification = notification

    def handle_alert(self, alert_in: Alert) -> None:
        alert_out = AlertEventOutcome(
            source_event_id=alert_in.alert_id,
            alert_id=alert_in.alert_id,
            monitored_service_id=alert_in.monitored_service_id,
            timestamp=alert_in.timestamp,
            message=alert_in.message,
        )
        try:
            with self._persistence.start_transaction():
                self._persistence.save_event(alert_out)
                status_event = self._persistence.get_last_status_event(alert_out.alert_id)
                if status_event and status_event.status == StatusOutcome.HEALTHY:
                    # Case 1
                    unhealthy_event = StatusEventOutcome(
                        status=StatusOutcome.UNHEALTHY,
                        source_event_id=alert_in.alert_id,
                        monitored_service_id=alert_in.monitored_service_id,
                    )
                    self._persistence.save_status_event(unhealthy_event)
                    policy = self._escalation_policy.get_policy(alert_out.monitored_service_id)
                    if len(policy.levels) > 0:
                        index = 0
                        level = policy.levels[index]
                        message = alert_out.message
                        for target in level.targets:
                            self._notification(target=target, message=message)
                            self._persistence.save_notification_event(
                                level_idx=index,
                                message=message,
                                recipient=target.recipient,
                                channel=target.__class__.__name__,
                            )

                    self._timer_service.set_timer(service_id=alert_out.monitored_service_id, delay=15 * 60)
        except Exception as e:
            self._persistence.rollback_transaction()
            raise SaveEventError(f"An error occurred during alert processing: {e}")
