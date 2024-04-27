from abc import abstractmethod, ABC
from typing import List


class NotificationService(ABC):
    @abstractmethod
    def notify_targets(self, targets: List[str], message: str) -> None:
        pass
