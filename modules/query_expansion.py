import logging
from parasel.core.context import Context
from modules.llm.inference import structured_inference
from jinja2 import Template
from pydantic import BaseModel
from typing import List

logger = logging.getLogger(__name__)

"""
쿼리 확장 기능의 module.
"""

class QueryExpansionOutput(BaseModel):
    queries: List[str]

async def query_expansion_by_language(context: Context, language: str, out_name: str, **kwargs):
    """
    언어별 쿼리 확장
    
    Args:
        context: Context 객체
        language: 확장할 언어 (ByArgs가 개별 값으로 전달: "en", "ko" 등)
        out_name: 결과를 저장할 키 이름
        **kwargs: 추가 파라미터
    """
    try:
        logger.info(f"[query_expansion] 시작: language={language}")
        
        # 원본 쿼리 가져오기
        query = context.get("query", "")
        
        prompt_by_language = {
            "en": "query_expansion_en.jinja2",
            "ko": "query_expansion_ko.jinja2",
            "ja": "query_expansion_ja.jinja2",
            "zh": "query_expansion_zh.jinja2",
            "es": "query_expansion_es.jinja2",
            "id": "query_expansion_id.jinja2",
            "vn": "query_expansion_vn.jinja2",
        }
        
        prompt_file = f"modules/llm/prompts/{prompt_by_language[language]}"
        
        with open(prompt_file, "r") as f:
            template = Template(f.read())
        prompt = template.render(query=query, num_queries=2)
        
        result = await structured_inference(prompt, "google/gemini-2.5-flash-lite", {"temperature": 0.4}, output_type=QueryExpansionOutput)
        
        # Context에 저장 (ByArgs가 자동으로 리스트에 누적)
        expanded_queries = result.output.queries
        context[out_name] = expanded_queries
        logger.info(f"[query_expansion] 완료: language={language}")
        
    except Exception as e:
        logger.error(f"[query_expansion] 에러 발생: language={language}, error={str(e)}", exc_info=True)
        raise