FROM python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# 依存関係のインストール
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# gunicornの追加（本番環境用Webサーバー）
RUN pip install gunicorn

# アプリケーションコードのコピー
COPY . /code/

# 静的ファイルの収集
RUN cd emt && python manage.py collectstatic --noinput

# コンテナ起動時にgunicornを実行
WORKDIR /code/emt
CMD exec gunicorn emt.wsgi:application --bind 0.0.0.0:$PORT