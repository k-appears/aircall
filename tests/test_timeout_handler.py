import logging

import pytest
from conftest import NOW_TIMESTAMP, PHONE_NUMBER, SERVICE_ID

from app.adapters.outcoming.persistency import PersistencyOutcomeAdapter
from app.adapters.outcoming.timer_service import TimerServiceOutcomeAdapter
from app.domain.entities.events import AckTimeoutIncomeEvent
from app.domain.services.timer_event_service import TimerEventService
from app.domain.value_objects.policy import EmailTargetPolicy, SMSTargetPolicy
from app.ports.outcoming.notification import NotificationOutcomePort
from app.ports.outcoming.persistency import (
    AcknowledgeEventOutcome,
    AckTimeoutEventOutcome,
    HealthyEventOutcome,
    SaveEventError,
    StatusEventOutcome,
    StatusOutcome,
)


def test_handle_ack_given_healthy(mocker, escalation_mock, mock_now):
    """Test case 2"""
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    handler = TimerEventService(
        escalation_policy=escalation_mock,
        persistence=persistence_mock,
        timer_service=timer_mock,
        notification=notification_mock,
    )

    persistence_mock.get_last_status_event.return_value = StatusEventOutcome(
        status=StatusOutcome.UNHEALTHY,
        source_event_id="67890",
        monitored_service_id=SERVICE_ID,
    )
    persistence_mock.get_last_notification_level_index.return_value = 0
    persistence_mock.get_events_by_alert_id.return_value = []

    ack = AckTimeoutIncomeEvent(
        event_id="12345",
        monitored_service_id=SERVICE_ID,
        source_alert_id="67890",
    )

    handler.handle_ack_timeout(ack)

    persistence_mock.get_last_status_event.assert_called_once_with("67890")
    persistence_mock.get_last_notification_level_index.assert_called_once_with("67890")
    persistence_mock.save_event.assert_called_once_with(
        AckTimeoutEventOutcome(
            source_event_id="12345",
            alert_id="67890",
            monitored_service_id=SERVICE_ID,
            timestamp=ack.timestamp,
        ),
    )
    timer_mock.set_timer.assert_called_once_with(delay=900, service_id=SERVICE_ID)
    assert notification_mock.call_count == 2
    assert notification_mock.call_args_list[0].kwargs == {
        "message": f"ACK timeout received and service {SERVICE_ID} still unhealthy.",
        "target": SMSTargetPolicy(recipient=PHONE_NUMBER),
    }
    assert notification_mock.call_args_list[1].kwargs == {
        "message": f"ACK timeout received and service {SERVICE_ID} still unhealthy.",
        "target": EmailTargetPolicy(recipient="test@test.com"),
    }


def test_handle_ack_given_unhealthy(mocker, escalation_mock):
    """Test case 3"""
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    handler = TimerEventService(
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
    persistence_mock.get_events_by_alert_id.return_value = [
        AcknowledgeEventOutcome(
            source_event_id="12345",
            alert_id="67890",
            monitored_service_id="service123",
            timestamp=1634212345,
        ),
    ]

    ack_timeout = AckTimeoutIncomeEvent(
        event_id="12345",
        timestamp=1634212345,
        source_alert_id="67890",
        monitored_service_id="service123",
    )

    handler.handle_ack_timeout(ack_timeout)

    persistence_mock.get_last_status_event.assert_called_once_with("67890")
    persistence_mock.get_last_notification_level_index.assert_not_called()
    persistence_mock.save_event.assert_called_once_with(
        AckTimeoutEventOutcome(
            source_event_id="12345",
            alert_id="67890",
            monitored_service_id="service123",
            timestamp=ack_timeout.timestamp,
        ),
    )
    timer_mock.set_timer.assert_not_called()
    notification_mock.assert_not_called()


def test_handle_ack_time_given_healthy(mocker, escalation_mock, mock_now):
    """Test case 5"""
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    handler = TimerEventService(
        escalation_policy=escalation_mock,
        persistence=persistence_mock,
        timer_service=timer_mock,
        notification=notification_mock,
    )

    persistence_mock.get_last_status_event.return_value = StatusEventOutcome(
        status=StatusOutcome.HEALTHY,
        source_event_id=mocker.Mock(),
        monitored_service_id=mocker.Mock(),
    )
    persistence_mock.get_events_by_alert_id.return_value = [
        HealthyEventOutcome(
            source_event_id="12345",
            alert_id="67890",
            monitored_service_id="service123",
        ),
    ]

    ack_timeout = AckTimeoutIncomeEvent(
        event_id="12345",
        source_alert_id="67890",
        monitored_service_id="service123",
    )

    handler.handle_ack_timeout(ack_timeout)

    persistence_mock.get_last_status_event.assert_called_once_with("67890")
    persistence_mock.save_event.assert_called_once_with(
        AckTimeoutEventOutcome(
            source_event_id=ack_timeout.event_id,
            alert_id=ack_timeout.source_alert_id,
            monitored_service_id=ack_timeout.monitored_service_id,
            timestamp=ack_timeout.timestamp,
        ),
    )
    timer_mock.set_timer.assert_not_called()
    notification_mock.assert_not_called()
    persistence_mock.save_status_event.assert_called_once_with(
        StatusEventOutcome(
            status=StatusOutcome.HEALTHY,
            source_event_id="67890",
            monitored_service_id="service123",
            timestamp=NOW_TIMESTAMP,
        ),
    )


def test_handle_ack_time_given_unhealthy_max_reached(mocker, escalation_mock, mock_now, caplog):
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    handler = TimerEventService(
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
    persistence_mock.get_events_by_alert_id.return_value = []
    persistence_mock.get_last_notification_level_index.return_value = len(
        escalation_mock.get_policy.return_value.levels,
    )

    ack_timeout = AckTimeoutIncomeEvent(
        event_id="12345",
        timestamp=1634212345,
        source_alert_id="67890",
        monitored_service_id="service123",
    )
    caplog.set_level(logging.INFO)

    handler.handle_ack_timeout(ack_timeout)

    persistence_mock.get_last_status_event.assert_called_once_with("67890")
    persistence_mock.get_last_notification_level_index.assert_called_once_with("67890")
    persistence_mock.save_event.assert_called_once_with(
        AckTimeoutEventOutcome(
            source_event_id="12345",
            alert_id="67890",
            monitored_service_id="service123",
            timestamp=ack_timeout.timestamp,
        ),
    )
    timer_mock.set_timer.assert_not_called()
    notification_mock.assert_not_called()
    assert "Last level reached for alert" in caplog.text


def test_handle_ack_time_exception_persistence(mocker, escalation_mock, mock_now):
    persistence_mock = mocker.MagicMock(spec=PersistencyOutcomeAdapter)
    timer_mock = mocker.Mock(spec=TimerServiceOutcomeAdapter)
    notification_mock = mocker.Mock(spec=NotificationOutcomePort)

    handler = TimerEventService(
        escalation_policy=escalation_mock,
        persistence=persistence_mock,
        timer_service=timer_mock,
        notification=notification_mock,
    )

    persistence_mock.save_event.side_effect = Exception("Error")

    ack_timeout = AckTimeoutIncomeEvent(
        event_id="12345",
        timestamp=1634212345,
        source_alert_id="67890",
        monitored_service_id="service123",
    )
    with pytest.raises(SaveEventError) as exe_info:
        handler.handle_ack_timeout(ack_timeout)

    assert str(exe_info.value) == "An error occurred during ack timeout processing: Error"
