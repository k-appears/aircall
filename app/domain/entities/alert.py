import time
from dataclasses import dataclass


@dataclass
class Alert:
    alert_id: str
    monitored_service_id: str
    timestamp: float = time.time()
    source: str = "Alerting Service"
    message: str = "Alerting Service has detected an issue"
