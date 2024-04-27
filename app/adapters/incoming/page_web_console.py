from app.domain.entities.events import AcknowledgeIncomeEvent, HealthyIncomeEvent
from app.ports.incoming.page_web_console import ConsoleIncomingPort


class ConsoleIncomingAdapter(ConsoleIncomingPort):
    def receive_event(self, event: HealthyIncomeEvent | AcknowledgeIncomeEvent) -> None:
        pass
