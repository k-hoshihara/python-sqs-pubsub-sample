# テスト戦略

## 概要

本プロジェクトは SQS のローカル環境として LocalStack を前提に設計しています。
しかし、LocalStack が[有償化](https://blog.localstack.cloud/the-road-ahead-for-localstack/)されたことにより、CI 環境では無償で利用できなくなりました。

そのため、CI 環境では暫定的に SQS 互換の OSS である [ElasticMQ](https://github.com/softwaremill/elasticmq) を使用して integration test を実行しています。

## ローカル環境

LocalStack を使用します。

```bash
docker compose up --build -d
docker compose --profile test run --rm integration-test
docker compose --profile test down
```

## CI 環境 (GitHub Actions)

`compose.ci.yaml` で LocalStack を ElasticMQ に override しています。

```bash
docker compose -f compose.yaml -f compose.ci.yaml up --build -d
docker compose -f compose.yaml -f compose.ci.yaml --profile test run --rm integration-test
docker compose -f compose.yaml -f compose.ci.yaml --profile test down
```

### override の仕組み

- `compose.yaml` の `localstack` サービスのイメージを `softwaremill/elasticmq-native` に差し替え
- publisher / subscriber / integration-test の `AWS_ENDPOINT_URL` を ElasticMQ のポートに変更
- アプリケーションコードの変更は不要（SQS 互換のため）

### 注意事項

- ElasticMQ は SQS の全機能をサポートしているわけではありません
- あくまで CI での暫定対応であり、ローカル開発では LocalStack の利用を推奨します