FROM python:3.12-slim

WORKDIR /workspace

# 必要なファイルをコピー
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY app /workspace/app/

# Pythonパスを設定
ENV PYTHONPATH=/workspace
