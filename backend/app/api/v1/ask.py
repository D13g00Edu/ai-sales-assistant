from fastapi import APIRouter
from app.modules.ai_query.services import NLQueryEngine
from app.schemas.requests import AskRequest
from app.schemas.responses import AskResponse

router = APIRouter()

@router.post("", response_model=AskResponse)
def ask_ai(request: AskRequest): return NLQueryEngine().translate_and_execute(request.question)
