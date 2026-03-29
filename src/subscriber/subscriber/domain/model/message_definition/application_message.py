from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ApplicationMessage:
    application_number: str
    application_type: str
    applied_at: datetime

    @classmethod
    def from_dict(cls, data: dict) -> "ApplicationMessage":
        return cls(
            application_number=data["application_number"],
            application_type=data["application_type"],
            applied_at=datetime.fromisoformat(data["applied_at"]),
        )

    def to_dict(self) -> dict:
        return {
            "application_number": self.application_number,
            "application_type": self.application_type,
            "applied_at": self.applied_at.isoformat(),
        }
