from abc import ABC, abstractmethod

from app.domain.value_objects.policy import EscalationPolicy


class EscalationPolicyOutcomePort(ABC):
    @abstractmethod
    def get_policy(self, service_id: str) -> EscalationPolicy:
        pass
