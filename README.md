# Voyager Sample - ベクトル検索デモ

Voyagerを使用したAirbnbデータセットのベクトル検索サンプルアプリケーションです。OpenAIのテキスト埋め込みを使用して、自然言語でAirbnb物件を検索できます。

## 主な特徴 🌟

- Voyagerを使用した高速なベクトル検索
- OpenAI text-embedding-3-smallモデルによる自然言語クエリの埋め込み
- MongoDB/airbnb_embeddings データセットを使用
- 価格範囲とWiFiの有無でフィルタリング可能

## 必要条件 📋

- Docker
- OpenAI API キー
- Make（オプション）

## セットアップと使用方法 🚀

1. 環境変数の設定:
```bash
export OPENAI_API_KEY=your_api_key_here
```

2. アプリケーションのビルド:
```bash
make build
```

3. インデックスの作成:
```bash
make create-index
```

4. 検索の実行:
```bash
make search
```

## 内部の動作 🔍

### インデックス作成プロセス
1. MongoDBのAirbnbデータセットをダウンロード
2. 各物件の事前計算された埋め込みベクトル（1536次元）を取得
3. Voyagerインデックスを構築し、メタデータと共に保存

### 検索プロセス
1. ユーザーの検索クエリをOpenAIのAPIで埋め込みベクトルに変換
2. Voyagerを使用して類似度の高い物件を検索
3. 指定された価格範囲とWiFi条件でフィルタリング
4. 結果を類似度スコアと共に表示

### ファイル構成
- `app/indexer.py`: インデックス作成ロジック
- `app/searcher.py`: 検索ロジック
- `app/utils.py`: OpenAI APIラッパー
- `app/models.py`: データモデル
- `app/cli.py`: CLIインターフェース

## ライセンス

このプロジェクトは [MITライセンス](LICENSE) の下で公開されています。
