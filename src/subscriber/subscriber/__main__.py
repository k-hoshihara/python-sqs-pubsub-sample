import logging

from subscriber.domain.service.subscribe_service import SubscribeService

logging.basicConfig(level=logging.INFO)


def main() -> None:
    service = SubscribeService()
    service.poll()


if __name__ == "__main__":
    main()
