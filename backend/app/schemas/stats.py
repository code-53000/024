from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class MineralStats(BaseModel):
    mineral_type: str
    count: int


class LocalityStats(BaseModel):
    locality: str
    count: int


class ProvinceStats(BaseModel):
    province: str
    count: int


class CrystalSystemStats(BaseModel):
    crystal_system: str
    count: int


class StatusStats(BaseModel):
    status: str
    count: int


class AcquisitionMethodStats(BaseModel):
    method: str
    count: int


class StatsResponse(BaseModel):
    total_specimens: int
    total_photos: int
    total_users: int
    total_value: float
    by_mineral: List[MineralStats]
    by_province: List[ProvinceStats]
    by_crystal_system: List[CrystalSystemStats]
    by_status: List[StatusStats]
    by_acquisition_method: List[AcquisitionMethodStats]
    recent_specimens: List[Dict[str, Any]]
