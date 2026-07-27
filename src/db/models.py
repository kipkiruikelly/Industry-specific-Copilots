import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    records: Mapped[List["EHRRecord"]] = relationship("EHRRecord", back_populates="tenant", cascade="all, delete-orphan")


class EHRRecord(Base):
    __tablename__ = "ehr_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(String(36), ForeignKey("tenants.id"), index=True, nullable=False)
    patient_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    mrn: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    diagnoses: Mapped[List[str]] = mapped_column(JSON, default=list)
    medications: Mapped[List[str]] = mapped_column(JSON, default=list)
    allergies: Mapped[List[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="records")


class ClinicalDocumentEmbedding(Base):
    __tablename__ = "clinical_document_embeddings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    patient_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    required_clearance: Mapped[int] = mapped_column(Integer, default=1, index=True)
    department: Mapped[str] = mapped_column(String(100), default="general", index=True)
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
