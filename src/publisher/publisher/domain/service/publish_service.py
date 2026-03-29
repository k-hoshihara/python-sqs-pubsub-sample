import json
import logging
import os
from datetime import datetime, timezone

import boto3

from publisher.domain.model.message_definition.application_message import ApplicationMessage
from publisher.repository.sqs_repository import SqsRepository

logger = logging.getLogger(__name__)


class PublishService:
    def __init__(self):
        self._repository = SqsRepository()

    def create_queue_if_not_exists(self) -> None:
        client = boto3.client("sqs")
        queue_name = os.environ["SQS_QUEUE_NAME"]
        try:
            client.get_queue_url(QueueName=queue_name)
        except client.exceptions.QueueDoesNotExist:
            client.create_queue(QueueName=queue_name)
            logger.info("Created queue: %s", queue_name)

    def publish(self) -> None:
        self.create_queue_if_not_exists()

        message = ApplicationMessage(
            application_number="APP-20260329-001",
            application_type="new",
            applied_at=datetime.now(timezone.utc),
        )

        self._repository.send(message)
        logger.info("Sent message: %s", json.dumps(message.to_dict()))
