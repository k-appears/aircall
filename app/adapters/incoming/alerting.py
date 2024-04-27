from app.domain.entities.alert import Alert
from app.ports.incoming.alerts import AlertingIncomingPort


class AlertingIncomingAdapter(AlertingIncomingPort):
    def receives_alert(self, alert: Alert) -> None:
        pass
