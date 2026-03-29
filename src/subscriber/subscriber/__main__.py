import json
import logging

from subscriber.domain.model.message_definition.application_message import ApplicationMessage
from subscriber.repository.redis_repository import RedisRepository
from subscriber.repository.sqs_repository import SqsRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    sqs_repository = SqsRepository()
    redis_repository = RedisRepository()

    logger.info("Subscriber started. Polling for messages...")

    while True:
        messages = sqs_repository.receive()

        for message in messages:
            body = json.loads(message["Body"])
            application_message = ApplicationMessage.from_dict(body)

            redis_repository.save(application_message)
            logger.info("Saved to Redis: %s", application_message.application_number)

            sqs_repository.delete(message["ReceiptHandle"])
            logger.info("Deleted from SQS: %s", application_message.application_number)


if __name__ == "__main__":
    main()
