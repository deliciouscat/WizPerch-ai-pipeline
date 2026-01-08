import logging
from parasel.core.context import Context
from modules.llm.embedding import get_cosine_similarity_scores

logger = logging.getLogger(__name__)

def formatize_page(page: str):
    return f"# {page['title']}\n\n {page['body']}"

def pack_result(score: float, index: int, distance: float, href: str):
    return {
        "score": float(score),  # numpy.float32 -> Python float
        "index": int(index),    # numpy.int64 -> Python int
        "distance": float(distance),  # numpy.float32 -> Python float
        "href": href,
    }

def normalized_scoring(context: Context, out_name: str, **kwargs):
    """
    Cosine Similarity Scoring with Normalization
    """
    logger.info("[normalized_scoring] 시작")
    
    query = context.get("query")
    pages = context.get("duckduckgo_search")
    
    formatted_pages = [formatize_page(p) for p in pages]
    distances, indices = get_cosine_similarity_scores(query, formatted_pages)
    distances, indices = distances[0], indices[0]

    # Score Normalization
    imax = indices.max()
    smooth_factor = 2
    normalized_scores = (smooth_factor+distances)**2+((imax-indices)/imax)
    normalized_scores /= (smooth_factor+1)**2 + 1

    # Packing
    results = [pack_result(score, index, distance, pages[index]["href"]) for score, index, distance in zip(normalized_scores, indices, distances)]
    context[out_name] = results
    print("log: cosine similarity scoring with normalization")