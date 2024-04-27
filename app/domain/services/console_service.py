from app.domain.entities.events import AcknowledgeIncomeEvent, HealthyIncomeEvent
from app.ports.outcoming.persistency import (
    AcknowledgeEventOutcome,
    HealthyEventOutcome,
    PersistencyOutcomePort,
    SaveEventError,
)


class ConsoleService:
    """
    On Acknowledgement Received:
        Store Acknowledged state.
    """

    def __init__(
        self,
        persistence: PersistencyOutcomePort,
    ):
        self._persistence = persistence

    def handle_acknowledge(self, ack_event_in: AcknowledgeIncomeEvent) -> None:
        """Added case: Store event"""
        ack_out = AcknowledgeEventOutcome(
            source_event_id=ack_event_in.event_id,
            alert_id=ack_event_in.source_alert_id,
            monitored_service_id=ack_event_in.monitored_service_id,
            timestamp=ack_event_in.timestamp,
        )
        try:
            with self._persistence.start_transaction():
                self._persistence.save_event(ack_out)
        except Exception as e:
            self._persistence.rollback_transaction()
            raise SaveEventError(f"An error occurred during ack processing: {e}")

    def handle_healthy(self, healthy_event: HealthyIncomeEvent) -> None:
        ack_out = HealthyEventOutcome(
            source_event_id=healthy_event.event_id,
            alert_id=healthy_event.source_alert_id,
            monitored_service_id=healthy_event.monitored_service_id,
            timestamp=healthy_event.timestamp,
        )
        try:
            with self._persistence.start_transaction():
                self._persistence.save_event(ack_out)
        except Exception as e:
            self._persistence.rollback_transaction()
            raise SaveEventError(f"An error occurred during ack processing: {e}")
