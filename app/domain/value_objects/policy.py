import time
from abc import ABC
from dataclasses import dataclass, field


class TargetPolicy(ABC):
    recipient: str


@dataclass(frozen=True)
class EmailTargetPolicy(TargetPolicy):
    recipient: str = field(default="", metadata={"recipient": "email_address"})


@dataclass(frozen=True)
class SMSTargetPolicy(TargetPolicy):
    recipient: str = field(default="", metadata={"recipient": "phone_number"})


@dataclass
class Level:
    targets: list[TargetPolicy]


@dataclass
class EscalationPolicy:
    service_id: str
    levels: list[Level]
    timestamp: float = time.time()
