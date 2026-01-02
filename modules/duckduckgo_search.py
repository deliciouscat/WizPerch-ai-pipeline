from parasel.core.context import Context
from llm.inference import inference
from jinja2 import Template

"""
쿼리를 받아서 DuckDuckGo 검색하는 module.
"""

def duckduckgo_search(context: Context, out_name: str, by_keys_input = None, **kwargs):
    """
    DuckDuckGo 검색 실행
    
    Args:
        context: Context 객체
        out_name: 결과를 저장할 키 이름
        **kwargs: 추가 파라미터
    """
    if by_keys_input:
        query = by_keys_input
    else:
        query = context.get("query_expansion")
    
    # 실제 구현 시:
    # from duckduckgo_search import DDGS
    # with DDGS() as ddgs:
    #     results = list(ddgs.text(query, max_results=10))
    
    # Placeholder output
    search_results = {
        "query": query,
        "results": [
            {
                "title": f"Result 1 for: {query}",
                "url": f"https://example.com/1?q={query}",
                "snippet": f"This is the first result for {query}",
            },
            {
                "title": f"Result 2 for: {query}",
                "url": f"https://example.com/2?q={query}",
                "snippet": f"This is the second result for {query}",
            },
            {
                "title": f"Result 3 for: {query}",
                "url": f"https://example.com/3?q={query}",
                "snippet": f"This is the third result for {query}",
            }
        ]
    }
    
    # Context에 저장 (ByKeys가 자동으로 리스트에 누적)
    context[out_name] = search_results
    print("log: duckduckgo search")