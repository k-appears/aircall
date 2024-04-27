import pytest

from app.adapters.outcoming.escalation_policy.adapter import EscalationOutcomeAdapter
from app.domain.value_objects.policy import (
    EmailTargetPolicy,
    EscalationPolicy,
    Level,
    SMSTargetPolicy,
)

NOW_TIMESTAMP = 1634212345.11111

EMAIL = "test@test.com"
PHONE_NUMBER = "1234567890"


@pytest.fixture
def mock_now(mocker):
    mocker.patch("time.time", return_value=NOW_TIMESTAMP)
    return mocker


@pytest.fixture
def escalation_mock(mocker):
    escalation_mock = mocker.Mock(spec=EscalationOutcomeAdapter)
    escalation_mock.get_policy.return_value = EscalationPolicy(
        service_id="service123",
        levels=[
            Level(
                targets=[
                    SMSTargetPolicy(recipient=PHONE_NUMBER),
                    EmailTargetPolicy(recipient=EMAIL),
                ],
            ),
        ],
    )
    return escalation_mock


SERVICE_ID = "service123"
