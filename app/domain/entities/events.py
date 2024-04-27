import time
from abc import ABC
from dataclasses import dataclass


@dataclass
class Event(ABC):
    event_id: str
    source_alert_id: str
    monitored_service_id: str
    timestamp: float = time.time()


@dataclass
class HealthyIncomeEvent(Event):
    source: str = "Web Console"


@dataclass
class AcknowledgeIncomeEvent(Event):
    source: str = "Web Console"


@dataclass
class AckTimeoutIncomeEvent(Event):
    source = "Timer Service"
