import os
from openai import OpenAI
import numpy as np
from typing import List


class EmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is not set")

    def get_embedding(self, text: str) -> List[float]:
        """OpenAIのtext-embedding-3-smallモデルを使用して埋め込みベクトルを生成"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small", input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {str(e)}")
