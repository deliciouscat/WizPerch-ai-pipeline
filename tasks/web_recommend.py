from parasel import ModuleAdapter,Serial, Parallel, ByArgs, ByKeys
from modules.query_expansion import query_expansion_by_language
from modules.ddg_search import duckduckgo_search
from modules.sort import exponential_weighted_gaussian
from parasel.core.context import Context

query_expansion = ModuleAdapter(
    query_expansion_by_language,
    out_name="query_expansion",
    )

duckduckgo_search = ModuleAdapter(
    duckduckgo_search,
    out_name="duckduckgo_search",
    )

sorting = ModuleAdapter(
    exponential_weighted_gaussian,
    out_name="sorted_results",
    )

def _list_flatten(context: Context, out_name: str, **kwargs):
    import logging
    logger = logging.getLogger(__name__)
    
    results = context.get("query_expansion")
    logger.info(f"[list_flatten] 입력: {results}")
    logger.info(f"[list_flatten] 입력 타입: {type(results)}")
    
    if isinstance(results, list) and len(results) > 0:
        # 첫 번째 항목이 리스트인지 확인 (중첩 리스트인 경우에만 평탄화)
        if isinstance(results[0], list):
            flattened = [item for sublist in results for item in sublist]
            logger.info(f"[list_flatten] 중첩 리스트 평탄화: {flattened}")
            context[out_name] = flattened
        else:
            # 이미 평탄한 리스트 (문자열 리스트)
            logger.info(f"[list_flatten] 이미 평탄한 리스트, 그대로 유지")
            context[out_name] = results
    else:
        logger.info(f"[list_flatten] 리스트가 아니거나 비어있음")
        context[out_name] = results
    
    logger.info(f"[list_flatten] 출력: {context.get(out_name)}")

list_flatten = ModuleAdapter(
    _list_flatten,
    out_name="query_expansion",
    )

web_recommend = Serial([
    Parallel([
        ByArgs(query_expansion, args={"language": ["en", "ko"]})
    ]),
    list_flatten,
    Parallel([
        ByKeys(duckduckgo_search, keys=["query_expansion"]),
    ]),
    sorting,
])