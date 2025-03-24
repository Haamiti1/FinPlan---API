from pydantic import BaseModel
from typing import Dict, List

class Projection(BaseModel):
    month: str
    projected_balance: float  # Corrigido: balance com "balance"

class SimulationInput(BaseModel):
    monthly_income: float
    monthly_expanses: Dict[str, float]
    monthly_investiment: float
    current_savings: float

class SimulationOutput(BaseModel):
    cash_flow_projection: List[Projection]
    suggestions: List[str]
