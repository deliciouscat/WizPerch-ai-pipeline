import os
import time
import numpy as np
import faiss
from openai import OpenAI

or_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=or_key,
)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
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

def get_cosine_similarity_index(texts: list[str], model_name: str = "qwen/qwen3-embedding-8b"):
    embeddings = get_embedding(texts, model_name)
    vectors = np.array([v.embedding for v in embeddings]).astype('float32')
    index = faiss.IndexFlatIP(vectors.shape[1])
    faiss.normalize_L2(vectors)
    index.add(vectors)
    return index