# KanriTimer 2.0 実装開始プロンプト

このプロンプトを新しいセッションでClaude Codeに渡して、KanriTimer 2.0の実装を開始してください。

---

## 📋 指示内容

あなたはKanriTimer 2.0の実装を担当するエンジニアです。以下の要件定義書に基づいて、ライブイベントのリハーサル進行管理システムを実装してください。

### プロジェクト概要

**プロジェクト名**: KanriTimer 2.0

**目的**: ライブイベントのリハーサル進行を効率的に管理し、担当者への自動LINE通知により円滑な運営を実現する

**実装期間**: 10日間（Phase 1のみ）

**技術スタック**:
- **フロントエンド**: React 18 + Vite + TailwindCSS
- **バックエンド**: Django 4.2 + Django REST Framework
- **リアルタイム通信**: Django Channels + WebSocket + Redis
- **データベース**: PostgreSQL
- **タスクキュー**: Celery + Celery Beat + Redis
- **外部API**: LINE Messaging API
- **インフラ**: Render

### 要件定義書

別途提供される `KanriTimer_v2_Requirements.md` を熟読してください。このドキュメントには以下が含まれています：

- システム概要とユーザー種類
- 機能要件（Phase 1とPhase 2）
- データモデル
- API設計
- 画面構成
- 実装スケジュール
- LINE連携の仕様
- デプロイ設定

### 実装の開始手順

#### ステップ1: 要件の確認
1. `KanriTimer_v2_Requirements.md` を読み込む
2. 不明点があれば質問する
3. Phase 1の範囲を確認する

#### ステップ2: プロジェクト構成の作成
以下の構成でプロジェクトを作成してください：

```
KanriTimer/
├── backend/                    # Django
│   ├── manage.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── home/                   # メインアプリ
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── consumers.py        # WebSocket
│   │   ├── tasks.py            # Celery Tasks
│   │   └── ...
│   └── requirements.txt
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── stores/             # Zustand
│   │   └── ...
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── docker-compose.yml
└── README.md
```

#### ステップ3: Day 1のタスクを開始
要件定義書の「7. 実装スケジュール」に従って、Day 1から順番に実装してください。

**Day 1の内容**:
- プロジェクト構成作成
- Docker Compose設定（PostgreSQL, Redis, Django, Celery, React）
- Django + DRF セットアップ
- React + Vite + TailwindCSS セットアップ
- 基本的な通信確認

### 重要な実装ポイント

#### 1. 認証機能は不要
- ログイン機能は実装しない
- PCとスマホの判定のみで権限を制御
- `react-device-detect` でデバイス判定

#### 2. タイマーの自動遷移
- タイマーが0:00になったら自動的に次のタイマーを開始
- WebSocketで全デバイスに配信

#### 3. 押し巻き表示
- 全体の押し巻きのみを表示
- 個別バンドの押し巻きは表示しない（ただしデータは記録する）

#### 4. LINE連携
- 名前ベースで自動連携
- メンバーがBotに名前を送信 → 自動でLINE User IDを保存

#### 5. WebSocketのリアルタイム配信
- タイマーの状態変更を1秒ごとに全デバイスに配信
- `timer.started`, `timer.paused`, `timer.updated`, `timer.completed` イベント

### 実装時の注意事項

1. **Phase 1の範囲を守る**
   - 管理部局（3人）のみ実装
   - 他の部局はPhase 2

2. **データモデルは拡張性を考慮**
   - Phase 2で他部局を追加しやすい設計

3. **エラーハンドリングを忘れずに**
   - LINE連携での同姓同名の処理
   - WebSocket切断時の再接続

4. **レスポンシブ対応**
   - PCとスマホで異なるUIを表示
   - TailwindCSSのブレークポイントを活用

### 質問事項

実装開始前に以下を確認してください：

1. **開発環境**
   - Docker Composeは使用可能か？
   - Node.js / npm / pnpm はインストール済みか？

2. **外部サービス**
   - LINE Developers Consoleのアカウントは準備できているか？
   - Renderのアカウントは作成済みか？

3. **優先順位**
   - 10日間で実装する場合、どの機能を優先するか？
   - テスト環境でのデプロイも含めるか？

### 実装の進め方

1. **毎日の進捗を確認**
   - Day 1〜10のスケジュールに従って進める
   - 各日の終わりに進捗を報告

2. **TodoWrite ツールを活用**
   - タスクを細分化して管理
   - 完了したタスクは即座にマーク

3. **並列実装を活用**
   - バックエンドとフロントエンドを並行して進める
   - 独立した機能は同時に実装

### 開始の合図

以下のメッセージで実装を開始してください：

**「KanriTimer 2.0の実装を開始します。まずはDay 1のタスクから始めます。」**

---

## 📚 参考資料

- 要件定義書: `KanriTimer_v2_Requirements.md`

---

**このプロンプトと要件定義書を新しいセッションに渡して、実装を開始してください。**
