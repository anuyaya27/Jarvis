from fastapi import APIRouter, Depends

from app.deps import get_sim_service
from app.schemas import SimulateRequest, SimulationResult
from app.sim.service import SimulationService

router = APIRouter(tags=["simulation"])


@router.post("/simulate", response_model=SimulationResult)
async def simulate(req: SimulateRequest, sim_service: SimulationService = Depends(get_sim_service)) -> SimulationResult:
    return sim_service.run(req)

