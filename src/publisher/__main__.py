import json
import logging
import os
from datetime import datetime, timezone

import boto3

from domain.model.message_definition.application_message import ApplicationMessage
from repository.sqs_repository import SqsRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_queue_if_not_exists() -> None:
    client = boto3.client("sqs")
    queue_name = os.environ["SQS_QUEUE_NAME"]
    try:
        client.get_queue_url(QueueName=queue_name)
    except client.exceptions.QueueDoesNotExist:
        client.create_queue(QueueName=queue_name)
        logger.info("Created queue: %s", queue_name)


def main() -> None:
    create_queue_if_not_exists()

    repository = SqsRepository()
    message = ApplicationMessage(
        application_number="APP-20260329-001",
        application_type="new",
        applied_at=datetime.now(timezone.utc),
    )

    repository.send(message)
    logger.info("Sent message: %s", json.dumps(message.to_dict()))


if __name__ == "__main__":
    main()
