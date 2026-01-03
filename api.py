"""FastAPI 서버: 웹 추천 파이프라인 API"""

import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# 환경 변수 로드 (.env 파일에서)
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "modules"))

from parasel.api.fastapi_app import create_app
from parasel.registry import TaskRegistry
from tasks.web_recommend import web_recommend

logger = logging.getLogger(__name__)


def create_api_app():
    """FastAPI 앱 생성"""
    logger.info("FastAPI 앱 생성 시작")
    
    # 레지스트리에 태스크 등록
    registry = TaskRegistry()
    registry.register(
        task_id="web_recommend",
        version="0.1.0",
        node=web_recommend,
        description="웹 추천 파이프라인: 쿼리 확장 → 검색 → 정렬",
        requires=["query"],
        produces=["query_expansion", "duckduckgo_search", "sorted_results"],
        tags=["web", "recommendation", "search"],
        mark_stable=True,
    )
    logger.info("태스크 등록 완료: web_recommend")
    
    # FastAPI 앱 생성
    app = create_app(
        registry=registry,
        title="WizPerch AI Pipeline API",
        description="웹 추천 파이프라인 API",
        version="0.1.0",
    )
    
    logger.info("FastAPI 앱 생성 완료")
    return app


# 앱 인스턴스 생성 (uvicorn이 이것을 import)
app = create_api_app()


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("WizPerch AI Pipeline API 서버 시작")
    print("=" * 80)
    print("\n사용 가능한 엔드포인트:")
    print("  - GET  /                    : API 정보")
    print("  - GET  /tasks               : 등록된 태스크 목록")
    print("  - GET  /tasks/{task_id}     : 특정 태스크 정보")
    print("  - POST /run/{task_id}       : 태스크 실행")
    print("  - GET  /health              : 헬스 체크")
    print("\n서버 주소: http://127.0.0.1:8000")
    print("API 문서: http://127.0.0.1:8000/docs")
    print("ReDoc: http://127.0.0.1:8000/redoc")
    print("=" * 80)
    print()
    
    uvicorn.run(app, host="127.0.0.1", port=8000)

