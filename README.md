# python-sqs-pubsub-sample

Python で Amazon SQS を使った Pub/Sub パターンのサンプルアプリケーションです。
Docker Compose で構成されており、ローカル環境に Python をインストールせずに動作確認できます。

## 概要

Publisher が SQS にメッセージを送信し、Subscriber が受信して Redis に保存する一連のフローを実装しています。
SQS には LocalStack を使用しています。

## 前提条件

- Docker / Docker Compose

## 前提事項

- LocalStack は[有償化](https://blog.localstack.cloud/the-road-ahead-for-localstack/)されたため、バージョンを 4.13.0 で固定しています

## クイックスタート

```bash
# サービス起動
docker compose up --build -d

# テスト実行
docker compose --profile test run --rm integration-test

# 後片付け
docker compose --profile test down
```

## ドキュメント

- [アーキテクチャ・設計方針](docs/ARCHITECTURE.md)
- [検証シナリオ・テスト仕様](docs/TEST_SCENARIO.md)
- [テスト戦略 (ローカル / CI)](docs/TEST_STRATEGY.md)
- [ライブラリ選定](docs/LIBRARY_SELECTION.md)
- [リトライポリシー](docs/RETRY_POLICY.md)
