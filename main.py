"""웹 추천 파이프라인 실행 메인 모듈"""

import sys
import json
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
# modules 디렉토리도 추가 (llm.inference import를 위해)
sys.path.insert(0, str(project_root / "modules"))

from parasel import Executor
from tasks.web_recommend import web_recommend


def setup_logging(verbose: bool = False) -> None:
    """로깅 설정"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )




def run_pipeline(query: str, languages: Optional[list] = None) -> Dict[str, Any]:
    """파이프라인 실행"""
    logger = logging.getLogger(__name__)
    
    initial_data = {"query": query}
    
    logger.info(f"파이프라인 실행 시작: query='{query}'")
    
    try:
        executor = Executor()
        result = executor.run(
            web_recommend,
            initial_data=initial_data
        )
        
        # 결과 정리
        output = {
            "success": result.success,
            "duration": result.duration,
            "query": query,
            "query_expansion": result.context.get("query_expansion", []),
            "duckduckgo_search": result.context.get("duckduckgo_search", []),
            "sorted_results": result.context.get("sorted_results"),
        }
        
        if not result.success and result.errors:
            output["errors"] = [str(error) for error in result.errors]
        
        logger.info(f"파이프라인 실행 완료: success={result.success}, duration={result.duration:.3f}초")
        
        return output
        
    except Exception as e:
        logger.error(f"파이프라인 실행 중 예외 발생: {e}", exc_info=True)
        return {
            "success": False,
            "duration": 0.0,
            "query": query,
            "errors": [str(e)]
        }


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="웹 추천 파이프라인 실행")
    parser.add_argument("query", type=str, help="검색할 쿼리")
    parser.add_argument("--output-file", type=str, help="결과를 저장할 파일 경로")
    parser.add_argument("--verbose", "-v", action="store_true", help="상세 로그 출력")
    
    args = parser.parse_args()
    
    setup_logging(verbose=args.verbose)
    result = run_pipeline(args.query)
    
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output_file:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output)
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
