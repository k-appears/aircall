import logging
import time

from app.domain.entities.events import AckTimeoutIncomeEvent
from app.ports.outcoming.escalation_policy import EscalationPolicyOutcomePort
from app.ports.outcoming.notification import NotificationOutcomePort
from app.ports.outcoming.persistency import (
    AcknowledgeEventOutcome,
    AckTimeoutEventOutcome,
    HealthyEventOutcome,
    PersistencyOutcomePort,
    SaveEventError,
    StatusEventOutcome,
    StatusOutcome,
)
from app.ports.outcoming.timer_service import TimerServiceOutcomePort

log = logging.getLogger(__name__)


class TimerEventService:
    """
    This class represents the Pager Service use cases. It is responsible for handling alerts and acknowledgements

    On Timeout Received:
        Check if Alert is not acknowledged.
        If last level not notified, notify next level and set timeout.
        If acknowledged, do nothing.
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

    def handle_ack_timeout(self, ack_timeout_event: AckTimeoutIncomeEvent) -> None:
        ack_timeout_out = AckTimeoutEventOutcome(
            source_event_id=ack_timeout_event.event_id,
            alert_id=ack_timeout_event.source_alert_id,
            monitored_service_id=ack_timeout_event.monitored_service_id,
            timestamp=ack_timeout_event.timestamp,
        )
        try:
            with self._persistence.start_transaction():
                self._persistence.save_event(ack_timeout_out)

                input_events = self._persistence.get_events_by_alert_id(ack_timeout_event.source_alert_id)
                status_event = self._persistence.get_last_status_event(ack_timeout_event.source_alert_id)
                if status_event and status_event.status == StatusOutcome.UNHEALTHY:
                    ack_found = any([isinstance(event, AcknowledgeEventOutcome) for event in input_events])
                    if not ack_found:
                        # Case 2
                        policy = self._escalation_policy.get_policy(ack_timeout_event.monitored_service_id)
                        last_index = self._persistence.get_last_notification_level_index(
                            ack_timeout_event.source_alert_id,
                        )
                        if last_index < len(policy.levels):
                            level = policy.levels[last_index]
                            index = last_index + 1
                            message = f"ACK timeout received and service {ack_timeout_event.monitored_service_id} still unhealthy."
                            for target in level.targets:
                                self._notification(target=target, message=message)
                                self._persistence.save_notification_event(
                                    level_idx=index,
                                    message=message,
                                    recipient=target.recipient,
                                    channel=target.__class__.__name__,
                                )
                            self._timer_service.set_timer(
                                service_id=ack_timeout_event.monitored_service_id,
                                delay=15 * 60,
                            )
                        else:
                            log.info(f"Last level reached for alert {ack_timeout_event.source_alert_id}")
                    # Case 3
                else:
                    # Case 5
                    healthy_found = any([isinstance(event, HealthyEventOutcome) for event in input_events])
                    if healthy_found:
                        status_event = StatusEventOutcome(
                            status=StatusOutcome.HEALTHY,
                            source_event_id=ack_timeout_event.source_alert_id,
                            monitored_service_id=ack_timeout_event.monitored_service_id,
                            timestamp=time.time(),
                        )
                        self._persistence.save_status_event(status_event)
        except Exception as e:
            self._persistence.rollback_transaction()
            raise SaveEventError(f"An error occurred during ack timeout processing: {e}")
