import json
import os

import boto3
from publisher.domain.model.message_definition.application_message import ApplicationMessage


class SqsRepository:
    def __init__(self):
        self._client = boto3.client("sqs")
        self._queue_name = os.environ["SQS_QUEUE_NAME"]

    def _get_queue_url(self) -> str:
        response = self._client.get_queue_url(QueueName=self._queue_name)
        return response["QueueUrl"]

    def send(self, message: ApplicationMessage) -> None:
        queue_url = self._get_queue_url()
        self._client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message.to_dict()),
        )
