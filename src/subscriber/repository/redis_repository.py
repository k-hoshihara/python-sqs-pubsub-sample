import json
import os

import redis
from domain.model.message_definition.application_message import ApplicationMessage


class RedisRepository:
    def __init__(self):
        self._client = redis.Redis(
            host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True,
        )

    def save(self, message: ApplicationMessage) -> None:
        self._client.set(
            message.application_number,
            json.dumps(message.to_dict()),
        )
