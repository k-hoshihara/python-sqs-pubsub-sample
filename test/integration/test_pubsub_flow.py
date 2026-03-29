import json
import os
import time

import boto3
import redis

SQS_QUEUE_NAME = os.environ.get("SQS_QUEUE_NAME", "sample-queue")


def _sqs_client():
    return boto3.client("sqs")


def _redis_client():
    return redis.Redis(
        host=os.environ.get("REDIS_HOST", "redis"),
        port=int(os.environ.get("REDIS_PORT", "6379")),
        decode_responses=True,
    )


def _wait_for_redis_key(client, key, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        value = client.get(key)
        if value is not None:
            return value
        time.sleep(1)
    return None


def _wait_for_empty_queue(client, queue_url, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        response = client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=1,
        )
        if not response.get("Messages"):
            return True
        time.sleep(1)
    return False


def test_publisher_sends_message_and_subscriber_saves_to_redis():
    redis_client = _redis_client()

    application_number = "APP-20260329-001"
    value = _wait_for_redis_key(redis_client, application_number)

    assert value is not None, f"Key '{application_number}' not found in Redis"

    data = json.loads(value)
    assert data["application_number"] == application_number
    assert data["application_type"] == "new"
    assert "applied_at" in data


def test_processed_message_is_deleted_from_sqs():
    sqs_client = _sqs_client()
    queue_url = sqs_client.get_queue_url(QueueName=SQS_QUEUE_NAME)["QueueUrl"]

    is_empty = _wait_for_empty_queue(sqs_client, queue_url)

    assert is_empty, "SQS queue still has messages after processing"