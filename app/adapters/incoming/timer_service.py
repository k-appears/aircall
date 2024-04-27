from app.domain.entities.events import AckTimeoutIncomeEvent
from app.ports.incoming.timer_service import TimerServiceIncomingPort


class TimerServiceIncomingAdapter(TimerServiceIncomingPort):
    def receives_acknowledge_timeout(self, ack_event: AckTimeoutIncomeEvent) -> None:
        pass
