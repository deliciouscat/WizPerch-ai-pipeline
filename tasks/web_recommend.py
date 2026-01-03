from parasel import ModuleAdapter,Serial, Parallel, ByArgs, ByKeys
from modules.query_expansion import query_expansion_by_language
from modules.ddg_search import duckduckgo_search
from modules.sort import exponential_weighted_gaussian

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

web_recommend = Serial([
    Parallel([
        ByArgs(query_expansion, args={"language": ["en", "ko"]})
    ]),
    Parallel([
        ByKeys(duckduckgo_search, keys=["query_expansion"]),
    ]),
    sorting,
])