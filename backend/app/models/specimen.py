from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..database import Base


class IdentificationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DISPUTED = "disputed"


class CrystalSystem(str, enum.Enum):
    ISOMETRIC = "isometric"
    TETRAGONAL = "tetragonal"
    ORTHORHOMBIC = "orthorhombic"
    HEXAGONAL = "hexagonal"
    TRIGONAL = "trigonal"
    MONOCLINIC = "monoclinic"
    TRICLINIC = "triclinic"
    AMORPHOUS = "amorphous"


class AcquisitionMethod(str, enum.Enum):
    PURCHASE = "purchase"
    MINING = "mining"
    GIFT = "gift"
    TRADE = "trade"
    EXCAVATION = "excavation"
    OTHER = "other"


class Specimen(Base):
    __tablename__ = "specimens"

    id = Column(Integer, primary_key=True, index=True)
    specimen_no = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    mineral_type = Column(String(100), index=True, nullable=False)
    variety = Column(String(100))
    locality = Column(String(200), index=True)
    province = Column(String(100), index=True)
    country = Column(String(100), index=True)
    mohs_hardness_min = Column(Float)
    mohs_hardness_max = Column(Float)
    crystal_system = Column(Enum(CrystalSystem), index=True)
    crystal_form = Column(String(200))
    color = Column(String(100))
    luster = Column(String(100))
    transparency = Column(String(100))
    cleavage = Column(String(200))
    fracture = Column(String(100))
    streak = Column(String(100))
    specific_gravity_min = Column(Float)
    specific_gravity_max = Column(Float)
    size = Column(String(100))
    weight = Column(Float)
    weight_unit = Column(String(20), default="g")
    acquisition_method = Column(Enum(AcquisitionMethod), index=True)
    acquisition_date = Column(DateTime)
    price = Column(Float)
    currency = Column(String(10), default="CNY")
    dealer = Column(String(200))
    description = Column(Text)
    notes = Column(Text)
    identification_status = Column(Enum(IdentificationStatus), default=IdentificationStatus.PENDING, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="specimens")
    photos = relationship("Photo", back_populates="specimen", cascade="all, delete-orphan", order_by="Photo.is_primary.desc(), Photo.created_at.asc()")
    identifications = relationship("Identification", back_populates="specimen", cascade="all, delete-orphan", order_by="Identification.created_at.desc()")
