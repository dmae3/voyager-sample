import voyager
import json
import os
from typing import List
from .models import SearchResult
from .utils import EmbeddingGenerator


class VectorSearcher:
    def __init__(self, index_path: str):
        # インデックスとメタデータの読み込み
        self.index = voyager.Index.load(index_path)
        metadata_path = os.path.join(os.path.dirname(index_path), "metadata.json")
        with open(metadata_path, "r") as f:
            metadata_list = json.load(f)
            # メタデータをインデックス番号をキーとした辞書に変換
            self.metadata = {str(i): item for i, item in enumerate(metadata_list)}
        self.embedding_generator = EmbeddingGenerator()

    def search(
        self,
        query: str,
        min_price: int,
        max_price: int,
        wifi_required: bool,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        テキスト検索を実行し、フィルタリングを適用
        """
        # クエリの埋め込み取得
        try:
            query_embedding = self.embedding_generator.get_embedding(query)
        except Exception as e:
            raise Exception(f"検索クエリの埋め込み生成に失敗しました: {str(e)}")

        # 検索実行（より多くの結果を取得してフィルタリング用のバッファとする）
        results = self.index.query(
            query_embedding, k=limit * 3  # フィルタリング後に十分な結果を確保するため
        )

        # 結果をフィルタリングして SearchResult オブジェクトに変換
        filtered_results = []
        ids, distances = results
        for i in range(len(ids)):
            id = str(ids[i])
            score = 1.0 / (1.0 + distances[i])  # 距離をスコアに変換
            metadata = self.metadata[id]  # インデックスIDを使用してメタデータを取得

            # 価格フィルター
            if not (min_price <= metadata["price"] <= max_price):
                continue

            # WiFiフィルター
            if wifi_required and "Wifi" not in metadata["amenities"]:
                continue

            filtered_results.append(
                SearchResult(
                    _id=metadata["_id"],
                    name=metadata["name"],
                    space=metadata["space"],
                    amenities=metadata["amenities"],
                    price=metadata["price"],
                    similarity_score=score,
                )
            )

            if len(filtered_results) >= limit:
                break

        return filtered_results
