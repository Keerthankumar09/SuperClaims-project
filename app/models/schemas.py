from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class BillDocument(BaseModel):
    type: Literal["bill"] = "bill"
    hospital_name: Optional[str] = None
    total_amount: Optional[float] = None
    date_of_service: Optional[date] = None
    items: Optional[List[dict]] = None

class DischargeSummary(BaseModel):
    type: Literal["discharge_summary"] = "discharge_summary"
    patient_name: Optional[str] = None
    diagnosis: Optional[str] = None
    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    doctor_name: Optional[str] = None

class IDCard(BaseModel):
    type: Literal["id_card"] = "id_card"
    policy_number: Optional[str] = None
    patient_name: Optional[str] = None
    dob: Optional[date] = None
    insurance_provider: Optional[str] = None

class ValidationResult(BaseModel):
    missing_documents: List[str] = Field(default_factory=list)
    discrepancies: List[str] = Field(default_factory=list)

class ClaimDecision(BaseModel):
    status: Literal["approved", "rejected", "pending"]
    reason: str
    confidence_score: Optional[float] = None

class ClaimResponse(BaseModel):
    documents: List[BillDocument | DischargeSummary | IDCard]
    validation: ValidationResult
    claim_decision: ClaimDecision
