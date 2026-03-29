# 検証シナリオ

## 概要

Publisher が SQS にメッセージを送信し、Subscriber が受信して Redis に保存する一連のフローを検証する。

## メッセージ定義

| フィールド              | 型      | 説明                             | 例                         |
|--------------------|--------|--------------------------------|---------------------------|
| application_number | string | 申し込み番号                         | APP-20260329-001          |
| application_type   | string | 申し込み種別 (new / change / cancel) | new                       |
| applied_at         | string | 申し込み日時 (ISO 8601)              | 2026-03-29T12:00:00+09:00 |

## フロー

1. `docker compose up` で LocalStack (SQS)、Redis、Publisher、Subscriber を起動
2. Publisher が SQS キューにメッセージを送信する
3. Subscriber が SQS キューをポーリングしてメッセージを受信する
4. Subscriber が受信したメッセージを Redis に保存する
5. Subscriber が SQS キューからメッセージを削除する

## テスト観点

- Publisher が送信したメッセージが SQS キューに入ること
- Subscriber が SQS キューからメッセージを取得できること
- Subscriber が Redis にメッセージを正しく保存すること
    - `application_number` をキーとして Redis から取得し、各フィールドの値が一致すること
- 処理済みメッセージが SQS キューから削除されていること

## テスト実行方法

1. 全サービスを起動する

   ```bash
   docker compose up --build -d
   ```

2. integration test を実行する

   ```bash
   docker compose --profile test run --rm integration-test
   ```

3. 後片付け

   ```bash
   docker compose --profile test down
   ```
