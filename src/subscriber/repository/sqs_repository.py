import logging
import os
import time

import boto3

logger = logging.getLogger(__name__)


class SqsRepository:
    def __init__(self):
        self._client = boto3.client("sqs")
        self._queue_name = os.environ["SQS_QUEUE_NAME"]

    def _get_queue_url(self) -> str:
        while True:
            try:
                response = self._client.get_queue_url(QueueName=self._queue_name)
                return response["QueueUrl"]
            except self._client.exceptions.QueueDoesNotExist:
                logger.info("Queue '%s' not found, retrying in 2s...", self._queue_name)
                time.sleep(2)

    def receive(self) -> list[dict]:
        queue_url = self._get_queue_url()
        response = self._client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20,
        )
        return response.get("Messages", [])

    def delete(self, receipt_handle: str) -> None:
        queue_url = self._get_queue_url()
        self._client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle,
        )
