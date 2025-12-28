from parasel.core.context import Context
from llm.inference import inference
from jinja2 import Template
"""
쿼리 확장 기능의 module.
"""


def query_expansion(context: Context, out_name: str, **kwargs):
    query = context.get("query")


def query_expansion_by_language(query: str, language: str):
    prompt_by_language = {
        "en": "query_expansion_en.jinja2",
        "ko": "query_expansion_ko.jinja2",
        "ja": "query_expansion_ja.jinja2",
        "zh": "query_expansion_zh.jinja2",
        "es": "query_expansion_es.jinja2",
        "id": "query_expansion_id.jinja2",
        "vn": "query_expansion_vn.jinja2",
    }
    prompt = Template(prompt_by_language[language]).render(query=query)
