import json
import logging

from subscriber.domain.model.message_definition.application_message import ApplicationMessage
from subscriber.repository.redis_repository import RedisRepository
from subscriber.repository.sqs_repository import SqsRepository

logger = logging.getLogger(__name__)


class SubscribeService:
    def __init__(self):
        self._sqs_repository = SqsRepository()
        self._redis_repository = RedisRepository()

    def poll(self) -> None:
        logger.info("Subscriber started. Polling for messages...")

        while True:
            messages = self._sqs_repository.receive()

            for message in messages:
                body = json.loads(message["Body"])
                application_message = ApplicationMessage.from_dict(body)

                self._redis_repository.save(application_message)
                logger.info("Saved to Redis: %s", application_message.application_number)

                self._sqs_repository.delete(message["ReceiptHandle"])
                logger.info("Deleted from SQS: %s", application_message.application_number)
