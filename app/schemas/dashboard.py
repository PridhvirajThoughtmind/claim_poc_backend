from typing import List, Optional, Dict, Any
from app.schemas.utils import StripStrBaseModel


class DashboardWidgets(StripStrBaseModel):
    earnings: float
    spend: float
    sales: float
    balance: float
    tasks: int
    projects: int


class DashboardCharts(StripStrBaseModel):
    barData: List[Dict[str, Any]]
    lineData: List[Dict[str, Any]]
    options: Dict[str, Any]


class DashboardPatientsSummary(StripStrBaseModel):
    totalPatients: int
    pendingClaims: int
    approvedClaims: int
