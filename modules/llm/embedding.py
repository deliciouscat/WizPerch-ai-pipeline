import os
import time
import numpy as np
import faiss
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

or_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=or_key,
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=8))
def get_embedding(texts: list[str], model_name: str = "qwen/qwen3-embedding-8b"):
    embedding = client.embeddings.create(
    #extra_headers={
    #    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. 오픈라우터 사용 랭킹 집계용. (사이트 주소)
    #    "X-Title": "<YOUR_SITE_NAME>", # Optional. 오픈라우터 사용 랭킹 집계용. (앱 이름)
    #},
    model=model_name,
    input=texts,
    encoding_format="float"
    )
    return embedding.data

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=12))
def get_cosine_similarity_scores(query: str, texts: list[str], model_name: str = "qwen/qwen3-embedding-8b"):
    embeddings = get_embedding([query, *texts], model_name)
    vectors = np.array([v.embedding for v in embeddings]).astype('float32')
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors[1:])  # query를 제외하고 texts만 인덱스에 추가
    distances, indices = index.search(vectors[0:1], k=len(texts))
    return distances, indices