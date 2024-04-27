from app.adapters.outcoming.persistency import PersistencyOutcomeAdapter
from app.domain.entities.events import AcknowledgeIncomeEvent
from app.domain.services.console_service import ConsoleService
from app.ports.outcoming.persistency import AcknowledgeEventOutcome


def test_handle_acknowledge(mocker, escalation_mock):
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)

    pager_service = ConsoleService(
        persistence=persistence_mock,
    )
    ack_income = AcknowledgeIncomeEvent(
        event_id="12345",
        timestamp=1634212345,
        source_alert_id="67890",
        monitored_service_id="service123",
    )

    pager_service.handle_acknowledge(ack_income)

    persistence_mock.save_event.assert_called_once_with(
        AcknowledgeEventOutcome(
            source_event_id=ack_income.event_id,
            alert_id=ack_income.source_alert_id,
            monitored_service_id=ack_income.monitored_service_id,
            timestamp=ack_income.timestamp,
        ),
    )
