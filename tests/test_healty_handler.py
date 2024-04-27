from app.adapters.outcoming.persistency import PersistencyOutcomeAdapter
from app.domain.entities.events import HealthyIncomeEvent
from app.domain.services.console_service import ConsoleService
from app.ports.outcoming.persistency import HealthyEventOutcome


def test_handle_healthy(mocker, escalation_mock):
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    handler = ConsoleService(persistence_mock)
    healthy_income = HealthyIncomeEvent(
        event_id="12345",
        timestamp=1634212345,
        source_alert_id="67890",
        monitored_service_id="service123",
    )

    handler.handle_healthy(healthy_income)

    persistence_mock.save_event.assert_called_once_with(
        HealthyEventOutcome(
            source_event_id=healthy_income.event_id,
            alert_id=healthy_income.source_alert_id,
            monitored_service_id=healthy_income.monitored_service_id,
            timestamp=healthy_income.timestamp,
        ),
    )
