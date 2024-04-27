import pytest
from conftest import EMAIL, PHONE_NUMBER

from app.adapters.outcoming.persistency import PersistencyOutcomeAdapter
from app.adapters.outcoming.timer_service import TimerServiceOutcomeAdapter
from app.domain.entities.alert import Alert
from app.domain.services.alert_service import AlertService
from app.domain.value_objects.policy import EmailTargetPolicy, SMSTargetPolicy
from app.ports.outcoming.notification import NotificationOutcomePort
from app.ports.outcoming.persistency import (
    AlertEventOutcome,
    SaveEventError,
    StatusEventOutcome,
    StatusOutcome,
)


def test_handle_alert_given_healthy(mocker, escalation_mock, mock_now):
    """Test case 1"""
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    handler = AlertService(
        escalation_policy=escalation_mock,
        persistence=persistence_mock,
        timer_service=timer_mock,
        notification=notification_mock,
    )

    persistence_mock.get_last_status_event.return_value = StatusEventOutcome(
        status=StatusOutcome.HEALTHY,
        monitored_service_id="service123",
    )

    alert = Alert(
        alert_id="12345",
        monitored_service_id="service123",
        message="Service is down!",
    )
    handler.handle_alert(alert)

    persistence_mock.get_last_status_event.assert_called_once_with("12345")
    persistence_mock.save_status_event.assert_called_once_with(
        StatusEventOutcome(
            status=StatusOutcome.UNHEALTHY,
            source_event_id="12345",
            monitored_service_id="service123",
        ),
    )
    timer_mock.set_timer.assert_called_once_with(delay=900, service_id="service123")
    assert notification_mock.call_count == 2
    assert notification_mock.call_args_list[0].kwargs == {
        "message": "Service is down!",
        "target": SMSTargetPolicy(recipient=PHONE_NUMBER),
    }
    assert notification_mock.call_args_list[1].kwargs == {
        "message": "Service is down!",
        "target": EmailTargetPolicy(recipient="test@test.com"),
    }
    assert persistence_mock.save_notification_event.call_count == 2
    assert persistence_mock.save_notification_event.call_args_list[0].kwargs == {
        "level_idx": 0,
        "message": "Service is down!",
        "recipient": PHONE_NUMBER,
        "channel": "SMSTargetPolicy",
    }
    assert persistence_mock.save_notification_event.call_args_list[1].kwargs == {
        "level_idx": 0,
        "message": "Service is down!",
        "recipient": EMAIL,
        "channel": "EmailTargetPolicy",
    }


def test_handle_alert_given_unhealthy(mocker, escalation_mock):
    """Test case 4"""
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    alert_service = AlertService(
        escalation_policy=escalation_mock,
        persistence=persistence_mock,
        timer_service=timer_mock,
        notification=notification_mock,
    )

    persistence_mock.get_last_status_event.return_value = StatusEventOutcome(
        status=StatusOutcome.UNHEALTHY,
        source_event_id=mocker.Mock(),
        monitored_service_id=mocker.Mock(),
        timestamp=mocker.Mock(),
    )

    alert = Alert(
        alert_id="12345",
        timestamp=1634212345,
        monitored_service_id="service123",
        message="Service is down!",
    )

    alert_service.handle_alert(alert)

    persistence_mock.get_last_status_event.assert_called_once_with("12345")

    persistence_mock.save_event.assert_called_once_with(
        AlertEventOutcome(
            source_event_id=alert.alert_id,
            alert_id=alert.alert_id,
            monitored_service_id=alert.monitored_service_id,
            timestamp=alert.timestamp,
            message=alert.message,
        ),
    )

    timer_mock.set_timer.assert_not_called()
    notification_mock.assert_not_called()
    persistence_mock.save_status_event.assert_not_called()


def test_handle_ack_time_exception_persistence(mocker, escalation_mock):
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    alert_service = AlertService(
        escalation_policy=escalation_mock,
        persistence=persistence_mock,
        timer_service=timer_mock,
        notification=notification_mock,
    )

    persistence_mock.save_event.side_effect = Exception("Error")

    alert = Alert(
        alert_id="12345",
        timestamp=1634212345,
        monitored_service_id="service123",
        message="Service is down!",
    )

    with pytest.raises(SaveEventError) as exe_info:
        alert_service.handle_alert(alert)

    assert str(exe_info.value) == "An error occurred during alert processing: Error"
