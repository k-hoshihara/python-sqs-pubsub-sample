import json
import logging
from datetime import datetime, timezone

from publisher.config.sqs_configurer import SqsConfigurer
from publisher.domain.model.message_definition.application_message import ApplicationMessage
from publisher.repository.sqs_repository import SqsRepository

logger = logging.getLogger(__name__)


class PublishService:
    def __init__(self):
        self._configurer = SqsConfigurer()
        self._repository = SqsRepository()

    def publish(self) -> None:
        self._configurer.create_queue_if_not_exists()

        message = ApplicationMessage(
            application_number="APP-20260329-001",
            application_type="new",
            applied_at=datetime.now(timezone.utc),
        )

        self._repository.send(message)
        logger.info("Sent message: %s", json.dumps(message.to_dict()))
