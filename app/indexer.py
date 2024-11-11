import voyager
from datasets import load_dataset
import numpy as np
import pandas as pd
from typing import Dict, Any
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.console import Console
import os
import time

console = Console()


class AirbnbIndexer:
    def __init__(self, cache_dir: str = "data/huggingface_cache"):
        os.makedirs(cache_dir, exist_ok=True)
        console.print(f"データセットをダウンロード中... 保存先: {cache_dir}")
        self.dataset = load_dataset("MongoDB/airbnb_embeddings", cache_dir=cache_dir)
        self.data = self.dataset["train"]

    def create_index(self, output_path: str):
        """text_embeddings（1536次元）を使用してインデックスを作成"""
        with Progress() as progress:
            # 1. データの準備
            prep_task = progress.add_task("データの準備...", total=100)

            # Embeddings の準備
            start_time = time.time()
            console.print("embeddings の準備...")
            embeddings = np.array(
                [item for item in self.data["text_embeddings"]], dtype=np.float32
            )
            console.print(f"embeddings の準備時間: {time.time() - start_time:.2f}秒")
            progress.update(prep_task, advance=50)

            num_vectors = len(embeddings)
            console.print(f"embeddings shape: {embeddings.shape}")

            # メタデータの準備（pandas使用）
            start_time = time.time()
            console.print("メタデータの準備...")

            # DataFrameに変換して一括処理
            df = pd.DataFrame(
                {
                    "_id": self.data["_id"],
                    "name": self.data["name"],
                    "space": self.data["space"],
                    "amenities": self.data["amenities"],
                    "price": self.data["price"],
                }
            )

            # 型変換を一括で実行
            df["_id"] = df["_id"].astype(int)
            df["price"] = df["price"].astype(int)

            # 辞書のリストに変換
            metadata_list = df.to_dict("records")
            console.print(f"メタデータの準備時間: {time.time() - start_time:.2f}秒")
            progress.update(prep_task, advance=50)

            # 2. インデックスの作成
            console.print("インデックスの作成を開始...")
            try:
                start_time = time.time()
                index = voyager.Index(
                    space=voyager.Space.Cosine,
                    num_dimensions=1536,
                    M=64,
                    ef_construction=400,
                    max_elements=num_vectors,
                    storage_data_type=voyager.StorageDataType.Float32,
                )
                console.print(
                    f"インデックスのインスタンス作成時間: {time.time() - start_time:.2f}秒"
                )

                # 3. ベクトルの一括追加（高速化）
                add_task = progress.add_task(
                    "ベクトルをインデックスに追加中...", total=1
                )

                # 全ベクトルを一度に追加（マルチスレッド処理）
                start_time = time.time()
                ids = list(range(num_vectors))
                index.add_items(
                    vectors=embeddings, ids=ids, num_threads=-1  # 全CPU使用
                )
                console.print(f"ベクトル追加時間: {time.time() - start_time:.2f}秒")
                progress.update(add_task, advance=1)

                # メタデータを別途保存
                console.print("メタデータを保存中...")
                import json

                start_time = time.time()
                metadata_path = os.path.join(
                    os.path.dirname(output_path), "metadata.json"
                )
                with open(metadata_path, "w") as f:
                    json.dump(metadata_list, f)
                console.print(f"メタデータ保存時間: {time.time() - start_time:.2f}秒")

                # 4. インデックスの保存
                save_task = progress.add_task("インデックスの保存中...", total=1)
                console.print("インデックスの保存を開始...")
                start_time = time.time()
                index.save(output_path)
                console.print(f"インデックス保存時間: {time.time() - start_time:.2f}秒")
                progress.update(save_task, advance=1)

                console.print(
                    f"[green]インデックスを {output_path} に保存しました[/green]"
                )
                console.print(
                    f"[green]メタデータを {metadata_path} に保存しました[/green]"
                )

            except Exception as e:
                console.print(f"[red]エラーの詳細: {str(e)}[/red]")
                raise Exception(f"インデックスの作成に失敗しました: {str(e)}")
