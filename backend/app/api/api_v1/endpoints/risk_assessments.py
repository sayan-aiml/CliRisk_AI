from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.risk_assessment import RiskAssessment
from app.schemas.risk_assessment import RiskAssessmentCreate, RiskAssessment, RiskAssessmentUpdate

router = APIRouter()

@router.post("/", response_model=RiskAssessment, status_code=status.HTTP_201_CREATED)
def create_risk_assessment(risk_assessment: RiskAssessmentCreate, db: Session = Depends(get_db)):
    db_risk_assessment = RiskAssessment(**risk_assessment.model_dump())
    db.add(db_risk_assessment)
    db.commit()
    db.refresh(db_risk_assessment)
    return db_risk_assessment

@router.get("/", response_model=List[RiskAssessment])
def read_risk_assessments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    risk_assessments = db.query(RiskAssessment).offset(skip).limit(limit).all()
    return risk_assessments

@router.get("/{risk_assessment_id}", response_model=RiskAssessment)
def read_risk_assessment(risk_assessment_id: int, db: Session = Depends(get_db)):
    db_risk_assessment = db.query(RiskAssessment).filter(RiskAssessment.id == risk_assessment_id).first()
    if db_risk_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    return db_risk_assessment

@router.put("/{risk_assessment_id}", response_model=RiskAssessment)
def update_risk_assessment(
    risk_assessment_id: int,
    risk_assessment_update: RiskAssessmentUpdate,
    db: Session = Depends(get_db)
):
    db_risk_assessment = db.query(RiskAssessment).filter(RiskAssessment.id == risk_assessment_id).first()
    if db_risk_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    
    update_data = risk_assessment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_risk_assessment, field, value)
    
    db.commit()
    db.refresh(db_risk_assessment)
    return db_risk_assessment

@router.delete("/{risk_assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_risk_assessment(risk_assessment_id: int, db: Session = Depends(get_db)):
    db_risk_assessment = db.query(RiskAssessment).filter(RiskAssessment.id == risk_assessment_id).first()
    if db_risk_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    db.delete(db_risk_assessment)
    db.commit()
    return None