import logging

from publisher.domain.service.publish_service import PublishService

logging.basicConfig(level=logging.INFO)


def main() -> None:
    service = PublishService()
    service.publish()


if __name__ == "__main__":
    main()
