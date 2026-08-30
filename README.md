# kanri-timer1.0（管理タイマー）

バンドライブ等のリハーサル進行を、曲・バンドごとにタイマーで管理するための Django アプリケーションです。タイマーの進行・一時停止・再開・スキップは、素の JavaScript（サーバーには依存しない）でブラウザ上で完結して動作します。

## 主な機能

- **タイマー管理**：バンド名・時間（分）・管理者1〜3を登録し、複数タイマーを順に実行できます（`/add` から追加、一覧の行クリックで編集・削除）。
- **タイマー実行（開始・一時停止・再開・スキップ）**：`emt/statics/app.js` の `startTimer` / `pauseTimer` / `resumeTimer` / `skipTimer` が `setInterval` でカウントダウンを行い、ボタンの `onclick`（`templates/pomodromo_timer.html`）から実際に呼び出されています。1つのタイマーが完了すると自動的に次のタイマーが開始します。
- **押し／巻き表示**：一時停止していた時間を積算し、進行が「押し」（遅れ）なのか「巻き」（巻き）なのかを表示します。
- **キーボードショートカット**：スペースキーで開始/一時停止/再開、→キーでスキップ（`app.js` の `keydown` ハンドラで実装）。
- **ドラッグ&ドロップでの並べ替え（AI実装）**：一覧テーブルの行をドラッグして順序を変更すると、`/reorder/` に POST してサーバー側の順序を更新します（実行中は行から `draggable` 属性が外れ、並べ替えできなくなります）。この機能はAIによって実装されました。

## 技術スタック

| 分類 | 技術 |
|---|---|
| バックエンド | Python / Django 4.2 |
| フロントエンド | Bootstrap 5 + 素の JavaScript（フレームワークなし） |
| データベース | SQLite（`db.sqlite3`） |
| 本番サーバー | Gunicorn（PythonAnywhere へのデプロイを想定した設定） |

> `requirements.txt` には `mysqlclient` が残っていますが、実際の `DATABASES` 設定（`emt/emt/settings.py`）は SQLite です。`docker-compose.yml` にも MySQL コンテナ（`db`）の定義が残っていますが、アプリ側はこれを参照していません。コミット履歴（`mysql特有の処理をsqliteでできるように書き換えた`）から、MySQL 構成をやめて SQLite に切り替えた際の残骸と見られます。

## ディレクトリ構成

```
.
├── emt/
│   ├── emt/             # プロジェクト設定（settings.py, urls.py, asgi.py, wsgi.py）
│   ├── home/             # メインアプリ（モデル・ビュー・フォーム・URL）
│   ├── statics/
│   │   ├── app.js        # タイマー進行・操作・並べ替えのロジック
│   │   └── style.css
│   ├── templates/
│   │   └── pomodromo_timer.html  # メイン画面テンプレート
│   └── manage.py
├── docker-compose.yml    # devcontainer 用（現状 MySQL は未使用）
├── Dockerfile            # 本番ビルド用（gunicorn 起動）
├── requirements.txt
├── KanriTimer_v2_Requirements.md   # 後継版「KanriTimer 2.0」の要件定義書
└── KanriTimer_v2_Kickoff_Prompt.md # KanriTimer 2.0 実装用のキックオフプロンプト
```

## データモデル

`emt/home/models.py` の `Timers` モデルのみで構成されています。

| フィールド | 内容 |
|---|---|
| `band_name` | バンド名 |
| `minutes` | タイマー時間（分） |
| `item1` / `item2` / `item3` | 管理者1〜3 |
| `uuid` | 表示順（並べ替え・削除時の再採番に利用） |

## セットアップ（ローカル）

1. リポジトリを取得します。

   ```bash
   git clone git@github.com:Mizuir0/kanri-timer1.0.git
   cd kanri-timer1.0
   ```

2. 依存関係をインストールします（`mysqlclient` のビルドに失敗する場合は、実際には SQLite しか使っていないため `requirements.txt` から一時的に外しても動作します）。

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. マイグレーションを実行し、開発サーバーを起動します。

   ```bash
   cd emt
   python manage.py migrate
   python manage.py createsuperuser   # 管理画面からタイマーを登録する場合
   python manage.py runserver
   ```

4. ブラウザで以下にアクセスします。

   - メイン画面: http://127.0.0.1:8000/
   - タイマー追加: http://127.0.0.1:8000/add/
   - 管理画面: http://127.0.0.1:8000/admin/

### コンテナ（devcontainer）を使う場合

`docker-compose.yml` は VS Code Dev Containers 向けの構成で、`web` コンテナは `tail -f /dev/null` で起動したままになります。コンテナに入って上記の `manage.py` コマンドを手動で実行してください。MySQL コンテナ（`db`）は現状アプリからは使われていません。

## 主なURL

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/` | メイン画面（現在のタイマー・タイマー一覧） |
| GET/POST | `/add/` | タイマー追加 |
| GET/POST | `/edit/<timer_id>/` | タイマー編集 |
| GET | `/delete/<timer_id>/` | タイマー削除（削除後、表示順を詰め直す） |
| POST | `/reorder/` | ドラッグ&ドロップによる並べ替えをサーバーに反映 |

## 今後の展開（KanriTimer 2.0）

リポジトリ内の `KanriTimer_v2_Requirements.md` / `KanriTimer_v2_Kickoff_Prompt.md` に、本システムの後継として計画されている「KanriTimer 2.0」の要件定義書と実装キックオフ用プロンプトが含まれています。React + Vite + TailwindCSS のフロントエンド、Django REST Framework + Channels + Celery のバックエンド、LINE Messaging API 連携による担当者への自動通知などが構想されています（別リポジトリ `kanri-timer` はこの2.0構想に基づく実装途中のものです）。

## 注意事項

- 本番用の `SECRET_KEY` は環境変数 `SECRET_KEY` から読み込まれます（未設定時は開発用のデフォルト値が使われるため、本番運用時は必ず設定してください）。
- `ALLOWED_HOSTS` に `Mizuiro.pythonanywhere.com` が直書きされています。別ホストにデプロイする場合は書き換えが必要です。
