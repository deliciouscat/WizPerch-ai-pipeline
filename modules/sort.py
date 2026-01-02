from parasel.core.context import Context

def exponential_weighted_gaussian(context: Context, out_name: str, **kwargs):
    """
    Exponential Weighted Gaussian Sorting
    """
    results = context.get("duckduckgo_search")
    # 맨 뒤의 것을 앞으로 옮기는 placeholder output
    if isinstance(results, list) and len(results) > 0:
        context[out_name] = results[-1:] + results[:-1]
    else:
        # results가 딕셔너리이거나 다른 형태인 경우 그대로 반환
        context[out_name] = results
    print("log: exponential weighted gaussian sorting")