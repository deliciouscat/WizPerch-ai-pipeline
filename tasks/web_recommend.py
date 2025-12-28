from parasel import Serial, Parallel, ModuleAdapter
from modules.query_expansion import query_expansion_by_language
from modules.search.duckduckgo import duckduckgo_search
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

queries_by_language = [query_expansion(language) for language in ["en", "ko"]]

web_recommend = Serial([
    Parallel(queries_by_language),
    Parallel([
        duckduckgo_search(query_expansion("en")),
        duckduckgo_search(query_expansion("ko")),
    ]),
    sorting,
])