from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ApplicationMessage:
    application_number: str
    application_type: str
    applied_at: datetime

    def to_dict(self) -> dict:
        return {
            "application_number": self.application_number,
            "application_type": self.application_type,
            "applied_at": self.applied_at.isoformat(),
        }
