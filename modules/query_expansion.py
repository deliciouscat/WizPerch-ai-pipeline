from parasel.core.context import Context
from llm.inference import inference
from jinja2 import Template
"""
쿼리 확장 기능의 module.
"""

def query_expansion_by_language(context: Context, language: str, out_name: str, **kwargs):
    """
    언어별 쿼리 확장
    
    Args:
        context: Context 객체
        language: 확장할 언어 (ByArgs가 개별 값으로 전달: "en", "ko" 등)
        out_name: 결과를 저장할 키 이름
        **kwargs: 추가 파라미터
    """
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
    
    # 실제 구현 시:
    # with open(f"prompts/{prompt_by_language[language]}", "r") as f:
    #     template = Template(f.read())
    # prompt = template.render(query=query)
    # expanded_queries = inference(prompt)
    
    # Placeholder output (실제로는 LLM 결과)
    expanded_queries = [
        f"expanded_query_{language}_{i}_{query}" 
        for i in range(3)  # 언어당 3개 쿼리 생성
    ]
    
    # Context에 저장 (ByArgs가 자동으로 리스트에 누적)
    context[out_name] = expanded_queries
    print("log: query expansion")