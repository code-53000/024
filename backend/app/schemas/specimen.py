from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

from ..models.specimen import (
    IdentificationStatus,
    CrystalSystem,
    AcquisitionMethod
)


class SpecimenBase(BaseModel):
    name: str = Field(..., max_length=200)
    mineral_type: str = Field(..., max_length=100)
    variety: Optional[str] = Field(None, max_length=100)
    locality: Optional[str] = Field(None, max_length=200)
    province: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    mohs_hardness_min: Optional[float] = Field(None, ge=0, le=10)
    mohs_hardness_max: Optional[float] = Field(None, ge=0, le=10)
    crystal_system: Optional[CrystalSystem] = None
    crystal_form: Optional[str] = Field(None, max_length=200)
    color: Optional[str] = Field(None, max_length=100)
    luster: Optional[str] = Field(None, max_length=100)
    transparency: Optional[str] = Field(None, max_length=100)
    cleavage: Optional[str] = Field(None, max_length=200)
    fracture: Optional[str] = Field(None, max_length=100)
    streak: Optional[str] = Field(None, max_length=100)
    specific_gravity_min: Optional[float] = Field(None, ge=0)
    specific_gravity_max: Optional[float] = Field(None, ge=0)
    size: Optional[str] = Field(None, max_length=100)
    weight: Optional[float] = Field(None, ge=0)
    weight_unit: str = "g"
    acquisition_method: Optional[AcquisitionMethod] = None
    acquisition_date: Optional[datetime] = None
    price: Optional[float] = Field(None, ge=0)
    currency: str = "CNY"
    dealer: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    notes: Optional[str] = None


class SpecimenCreate(SpecimenBase):
    specimen_no: Optional[str] = Field(None, max_length=50)


class SpecimenUpdate(SpecimenBase):
    name: Optional[str] = Field(None, max_length=200)
    mineral_type: Optional[str] = Field(None, max_length=100)
    identification_status: Optional[IdentificationStatus] = None


class SpecimenResponse(SpecimenBase):
    id: int
    specimen_no: str
    identification_status: IdentificationStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SpecimenListResponse(BaseModel):
    items: List[SpecimenResponse]
    total: int
    page: int
    page_size: int
