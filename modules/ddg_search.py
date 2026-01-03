from parasel.core.context import Context
from duckduckgo_search import DDGS
from pydantic import BaseModel
from typing import List

class DuckDuckGoSearchOutput(BaseModel):
    results: List[str]

"""
쿼리를 받아서 DuckDuckGo 검색하는 module.
"""

async def duckduckgo_search(context: Context, out_name: str, by_keys_input = None, **kwargs):
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
    
    # DDGS는 동기 함수이지만, async 함수 내에서 호출 가능
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=10))
    
    # Context에 저장 (ByKeys가 자동으로 리스트에 누적)
    context[out_name] = results
    print("log: duckduckgo search")

