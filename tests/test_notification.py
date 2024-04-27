import pytest
from conftest import EMAIL

from app.domain.value_objects.policy import EmailTargetPolicy
from app.ports.outcoming.notification import NotificationOutcomePort


def test_notification_fail(mocker):
    notification_port = NotificationOutcomePort()
    with pytest.raises(ValueError) as exc:
        notification_port(target=mocker.Mock, message="test")

    assert str(exc.value) == f"Key '{mocker.Mock}' not found as notification"


def test_notification():
    notification_port = NotificationOutcomePort()
    assert notification_port(target=EmailTargetPolicy(recipient=EMAIL), message="test") is None
