from app.ports.outcoming.timer_service import TimerServiceOutcomePort


class TimerServiceOutcomeAdapter(TimerServiceOutcomePort):

    def set_timer(self, service_id: str, delay: int) -> None:
        pass
