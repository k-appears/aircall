from abc import abstractmethod

from app.domain.value_objects.policy import EscalationPolicy
from app.ports.outcoming.escalation_policy import EscalationPolicyOutcomePort


class EscalationOutcomeAdapter(EscalationPolicyOutcomePort):
    @abstractmethod
    def get_policy(self, service_id: str) -> EscalationPolicy:
        pass
