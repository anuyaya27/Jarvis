from fastapi import APIRouter, Depends

from app.deps import get_sim_service
from app.schemas import DecisionSpec, DecisionSpecRequest, SimulateRequest, SimulationResult
from app.sim.service import SimulationService

router = APIRouter(tags=["simulation"])


@router.post("/decision/spec", response_model=DecisionSpec)
async def decision_spec(
    req: DecisionSpecRequest,
    sim_service: SimulationService = Depends(get_sim_service),
) -> DecisionSpec:
    source_text = req.decision_text or req.transcript or ""
    return sim_service.extract_decision_spec(source_text)


@router.post("/simulate", response_model=SimulationResult)
async def simulate(req: SimulateRequest, sim_service: SimulationService = Depends(get_sim_service)) -> SimulationResult:
    return sim_service.run(req)
