from parasel import ModuleAdapter,Serial, Parallel, ByArgs, ByKeys
from modules.query_expansion import query_expansion_by_language
from modules.ddg_search import duckduckgo_search
from modules.scoring import normalized_scoring
from parasel.core.context import Context

query_expansion = ModuleAdapter(
    query_expansion_by_language,
    out_name="query_expansion",
    )

duckduckgo_search = ModuleAdapter(
    duckduckgo_search,
    out_name="duckduckgo_search",
    )

scoring = ModuleAdapter(
    normalized_scoring,
    out_name="scored_results",
    )

def _list_flatten(context: Context, out_name: str, in_name: str = None, **kwargs):
    import logging
    logger = logging.getLogger(__name__)
    
    # in_name이 제공되지 않으면 out_name을 사용 (기본 동작)
    key_to_read = in_name if in_name is not None else out_name
    results = context.get(key_to_read)

    if isinstance(results, list) and len(results) > 0:
        # 첫 번째 항목이 리스트인지 확인 (중첩 리스트인 경우에만 평탄화)
        if isinstance(results[0], list):
            flattened = [item for sublist in results for item in sublist]
            context[out_name] = flattened
        else:
            # 이미 평탄한 리스트 (문자열 리스트)
            context[out_name] = results
    else:
        context[out_name] = results

list_flatten_query_expansion = ModuleAdapter(
    _list_flatten,
    out_name="query_expansion",
    )

list_flatten_duckduckgo_search = ModuleAdapter(
    _list_flatten,
    out_name="duckduckgo_search",
    in_name="duckduckgo_search",
    )

web_recommend = Serial([
    Parallel([
        ByArgs(query_expansion, args={"language": ["en", "ko"]})
    ]),
    list_flatten_query_expansion,
    Parallel([
        ByKeys(duckduckgo_search, keys=["query_expansion"]),
    ]),
    list_flatten_duckduckgo_search,
    scoring,
]).expose(
    expose_keys=[
        #"query_expansion",
        #"duckduckgo_search",
        "scored_results",
    ],
)