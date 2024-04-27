import logging

from app.domain.entities.events import AckTimeoutIncomeEvent
from app.domain.services.timer_event_service import TimerEventService
from app.ports.outcoming.persistency import SaveEventError

log = logging.getLogger(__name__)


class ProcessAckLaterAckTimeoutCase:
    def __init__(self, timer_event_service: TimerEventService):
        self._timer_event_service = timer_event_service

    def execute(self, ack_timeout_event: AckTimeoutIncomeEvent) -> dict[str, str | bool]:
        try:
            self._timer_event_service.handle_ack_timeout(ack_timeout_event)
        except SaveEventError as save_error:
            log.error(f"Saving from ack timeout input: {ack_timeout_event}, error: {save_error}")
            return {"success": False, "message": "Error processing alert"}
        except Exception as e:
            log.error(f"Error processing ack timeout: {ack_timeout_event}, error: {e}")
            return {"success": False, "message": "Error processing alert"}

        return {"success": True, "message": "Ack timeout processed successfully"}
