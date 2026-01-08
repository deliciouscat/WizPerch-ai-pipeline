import os
import logging
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic import BaseModel
from typing import Type, TypeVar, Any, Optional

logger = logging.getLogger(__name__)

'''
이미 완성된 프롬프트를 받아서 인퍼런스

# input
model_name: str
prompt: str

# output

'''

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=12))
async def inference(prompt: str, model_name: str, model_settings: dict, system_prompt: Optional[str] = None):
    model = OpenAIModel(
        model_name,
        provider=OpenRouterProvider(api_key=os.getenv("OPENROUTER_API_KEY")),
    )
    agent_kwargs = {
        "model": model,
        "model_settings": model_settings,
    }
    if system_prompt: agent_kwargs["system_prompt"] = system_prompt
    
    agent = Agent(
        **agent_kwargs,
    )
    result = await agent.run(prompt)
    return result

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=12))
async def structured_inference(
    prompt: str, 
    model_name: str, 
    model_settings: dict, 
    system_prompt: Optional[str] = None,
    output_type: Optional[Type[BaseModel]] = None
) -> Any:
    """구조화된 출력을 위한 새로운 inference 함수"""
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY 환경 변수가 설정되지 않았습니다.")
        
        model = OpenAIModel(
            model_name,
            provider=OpenRouterProvider(api_key=api_key),
        )
        
        agent_kwargs = {
            "model": model,
            "model_settings": model_settings,
            "output_type": output_type  # 구조화된 출력 타입 지정
        }
        if system_prompt: 
            agent_kwargs["system_prompt"] = system_prompt
        
        agent = Agent(**agent_kwargs)
        result = await agent.run(prompt)
        
        return result
        
    except Exception as e:
        logger.error(f"[structured_inference] 에러 발생: error={str(e)}", exc_info=True)
        raise