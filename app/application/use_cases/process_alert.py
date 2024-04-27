import logging

from app.domain.entities.alert import Alert
from app.domain.services.alert_service import AlertService
from app.ports.outcoming.persistency import SaveEventError

log = logging.getLogger(__name__)


class ProcessAlertUseCase:
    def __init__(self, alert_service: AlertService):
        self._alert_service = alert_service

    def execute(self, alert: Alert) -> dict[str, str | bool]:
        try:
            self._alert_service.handle_alert(alert)
        except SaveEventError as save_error:
            log.error(f"Saving from alert input: {alert}, error: {save_error}")
            return {"success": False, "message": "Error processing alert"}
        except Exception as e:
            log.error(f"Error processing alert: {alert}, error: {e}")
            return {"success": False, "message": "Error processing alert"}

        return {"success": True, "message": "Alert processed successfully"}
