from fastapi import APIRouter, Depends

from app.deps import get_agent_provider
from app.providers.interfaces import AgentAutomationProvider
from app.schemas import PlaybookRequest

router = APIRouter(prefix="/playbook", tags=["playbook"])


@router.post("/run")
async def run_playbook(req: PlaybookRequest, agent: AgentAutomationProvider = Depends(get_agent_provider)) -> dict:
    return agent.run_playbook(req.name, req.payload)

