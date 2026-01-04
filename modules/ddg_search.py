import logging
from parasel.core.context import Context
from ddgs import DDGS
from pydantic import BaseModel
from typing import List

logger = logging.getLogger(__name__)

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
        by_keys_input: ByKeys에서 전달하는 개별 쿼리 (문자열) - deprecated
        **kwargs: 추가 파라미터 (ByKeys는 'input' 키로 전달)
    """
    logger.info(f"[duckduckgo_search] 시작")
    logger.info(f"[duckduckgo_search] kwargs: {kwargs}")
    
    # ByKeys는 'input' 키로 개별 항목을 전달
    if 'input' in kwargs:
        query = kwargs['input']
        logger.info(f"[duckduckgo_search] kwargs['input'] 사용: {query}")
    elif by_keys_input is not None:
        query = by_keys_input
        logger.info(f"[duckduckgo_search] by_keys_input 사용: {query}")
    else:
        query = context.get("query_expansion")
        logger.info(f"[duckduckgo_search] context에서 가져옴: {query}")
    
    # query가 문자열인지 확인
    if not isinstance(query, str):
        logger.error(f"[duckduckgo_search] query가 문자열이 아닙니다: {type(query)}")
        raise TypeError(f"query는 문자열이어야 합니다. 받은 타입: {type(query)}, 값: {query}")
    
    logger.info(f"[duckduckgo_search] 검색 쿼리: '{query}'")
    
    # DDGS는 동기 함수이지만, async 함수 내에서 호출 가능
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=10))
    
    logger.info(f"[duckduckgo_search] 검색 완료: {len(results)}개 결과")
    
    # Context에 저장 (ByKeys가 자동으로 리스트에 누적)
    context[out_name] = results
    logger.info(f"[duckduckgo_search] 완료")

