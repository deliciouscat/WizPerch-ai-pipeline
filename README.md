# 기능 목록
✅ 구현됨 ❌ 구현필요
- 웹 추천
- 유저특성추출 / 칭호작명
- 요약 / 인덱싱
- 필터링

## 웹 추천

```
Serial([
    Parallel([
        영어 쿼리확장,
        *유저설정언어 쿼리확장,
    ]),
    Parallel([
        *각 쿼리로 DuckDuckGo 검색,
    ]),
    Ranking 프로세스,
    출력 양식화
])
```


# 사용
```bash
# api 서버 열기
uv run uvicorn api:app --host 0.0.0.0 --port 8000
# 태스크 목록 조회
curl http://127.0.0.1:8000/tasks
# 파이프라인 실행
curl -X POST "http://127.0.0.1:8000/run/web_recommend" \
  -H "Content-Type: application/json" \
  -d '{"data": {"query": "machine learning"}, "version": "0.1.0"}'
```