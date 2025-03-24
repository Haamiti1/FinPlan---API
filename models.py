from pydantic import BaseModel
from typing import Dict, List

class SimulationInput(BaseModel):
    user_id: str
    monthly_income: float
    monthly_expanses: Dict[str, float]
    current_savings: float
    monthly_investiment: float

class Projection(BaseModel):
    moth: str
    projected_balance: float

class SimulationOutput(BaseModel):
    cash_flow_projection: List[Projection]
    suggestions: List[str]