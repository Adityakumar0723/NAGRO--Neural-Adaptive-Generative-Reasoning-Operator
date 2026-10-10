"""Code endpoints for NAGRO 4.1."""

from __future__ import annotations
from fastapi import APIRouter, Request

from nagro.core.models import CodeRequest, ChatRequest, TaskType

router = APIRouter()


@router.post("/code")
async def code_assist(request: CodeRequest, req: Request):
    engine = req.app.state.engine
    prompt = f"[{request.action.upper()}] "
    if request.language:
        prompt += f"[Language: {request.language}] "
    prompt += request.prompt
    if request.context:
        prompt += f"\n\nContext:\n{request.context}"

    chat_req = ChatRequest(
        message=prompt,
        task_type=TaskType.CODE,
    )
    response = await engine.process(chat_req)
    return response


@router.post("/code/execute")
async def execute_code(request: CodeRequest, req: Request):
    from nagro.tools.code_executor import execute_python
    if request.language and request.language.lower() != "python":
        return {"error": f"Only Python execution is supported, got: {request.language}"}
    result = execute_python(request.prompt)
    return result
