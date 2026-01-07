from parasel.core.context import Context
import numpy as np
import faiss

def normalize_and_sort(context: Context, out_name: str, **kwargs):
    """
    Exponential Weighted Gaussian Sorting
    """
    results = context.get("duckduckgo_search")
    
    vectors = np.array([v.embedding for v in embedding.data]).astype('float32')
    index = faiss.IndexFlatIP(vectors.shape[1])     # inner product
    faiss.normalize_L2(vectors)     # 벡터 정규화 (코사인 유사도 = 정규화된 벡터의 내적)
    index.add(vectors)              # 인덱스에 벡터 추가
    
    context[out_name] = results
    print("log: exponential weighted gaussian sorting")