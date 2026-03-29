import logging
import os

import boto3

logger = logging.getLogger(__name__)


class SqsConfigurer:
    def __init__(self):
        self._client = boto3.client("sqs")
        self._queue_name = os.environ["SQS_QUEUE_NAME"]

    def create_queue_if_not_exists(self) -> None:
        try:
            self._client.get_queue_url(QueueName=self._queue_name)
        except self._client.exceptions.QueueDoesNotExist:
            self._client.create_queue(QueueName=self._queue_name)
            logger.info("Created queue: %s", self._queue_name)
