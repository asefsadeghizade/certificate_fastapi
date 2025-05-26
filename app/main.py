from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .models import Certificate
from .database import get_db
from pydantic import BaseModel
from datetime import date
from typing import Optional


app = FastAPI()


API_VERSION = "v1"


class ValidateRequest(BaseModel):
    unique_code: str


class ValidateResponse(BaseModel):
    unique_code: str
    is_valid: bool
    message: str

    # Extra certificate details
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    course_name: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    status: Optional[str] = None


@app.get("/certificates")
def list_certificates(db: Session = Depends(get_db)):
    certs = db.query(Certificate).all()
    results = []
    for cert in certs:
        results.append({
            "id": str(cert.id),
            "student": {
                "id": str(cert.student.id),
                "student_id": cert.student.student_id,
                "first_name": cert.student.first_name,
                "last_name": cert.student.last_name,
                "full_name": cert.student.full_name,
                "email": cert.student.email,
                "date_of_birth": cert.student.date_of_birth.isoformat() if cert.student.date_of_birth else None,
                "created_at": cert.student.created_at.isoformat() if cert.student.created_at else None,
                "updated_at": cert.student.updated_at.isoformat() if cert.student.updated_at else None,
            },
            "course": {
                "id": str(cert.course.id),
                "name": cert.course.name,
                "description": cert.course.description,
                "duration": cert.course.duration,
                "created_at": cert.course.created_at.isoformat() if cert.course.created_at else None,
                "updated_at": cert.course.updated_at.isoformat() if cert.course.updated_at else None,
            },
            "issue_date": cert.issue_date.isoformat() if cert.issue_date else None,
            "expiry_date": cert.expiry_date.isoformat() if cert.expiry_date else None,
            "unique_code": cert.unique_code,
            "status": cert.status,
            "created_at": cert.created_at.isoformat() if cert.created_at else None,
            "updated_at": cert.updated_at.isoformat() if cert.updated_at else None,
            "signature": cert.signature,
        })
    return {"count": len(results), "results": results}


@app.get("/certificate/{unique_code}")
def get_certificate(unique_code: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(
        Certificate.unique_code == unique_code).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return {
        "id": str(cert.id),
        "student": {
            "id": str(cert.student.id),
            "student_id": cert.student.student_id,
            "first_name": cert.student.first_name,
            "last_name": cert.student.last_name,
            "full_name": cert.student.full_name,
            "email": cert.student.email,
            "date_of_birth": cert.student.date_of_birth.isoformat() if cert.student.date_of_birth else None,
            "created_at": cert.student.created_at.isoformat(),
            "updated_at": cert.student.updated_at.isoformat(),
        },
        "course": {
            "id": str(cert.course.id),
            "name": cert.course.name,
            "description": cert.course.description,
            "duration": cert.course.duration,
            "created_at": cert.course.created_at.isoformat(),
            "updated_at": cert.course.updated_at.isoformat(),
        },
        "issue_date": cert.issue_date.isoformat(),
        "expiry_date": cert.expiry_date.isoformat() if cert.expiry_date else None,
        "unique_code": cert.unique_code,
        "status": cert.status,
        "created_at": cert.created_at.isoformat(),
        "updated_at": cert.updated_at.isoformat(),
        "signature": cert.signature,
    }


@app.get(f"api/{API_VERSION}/")
def read_root():
    return {"message": "Hello World"}


@app.get(f"/api/{API_VERSION}/health")
def health_check():
    return {"status": "ok"}


'''
@app.get("/validate", response_model=ValidateResponse)
def validate_certificate(code: str = Query(..., alias="code"), db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(
        Certificate.unique_code == code).first()
    if not cert:
        return ValidateResponse(
            unique_code=code,
            is_valid=False,
            message="Certificate not found"
        )

    if not cert.verify_signature():
        return ValidateResponse(
            unique_code=code,
            is_valid=False,
            message="Invalid certificate signature"
        )

    return ValidateResponse(
        unique_code=code,
        is_valid=True,
        message="Certificate is valid"
    )
'''

# temp

'''
@app.post("/admin/fix-signature")
def fix_signature(code: str, db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(
        Certificate.unique_code == code).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    old_sig = cert.signature
    new_sig = cert.generate_signature()
    cert.signature = new_sig
    db.commit()

    return {
        "unique_code": cert.unique_code,
        "old_signature": old_sig,
        "new_signature": new_sig,
        "message": "Signature updated successfully"
    }
'''


@app.get(f"api/{API_VERSION}/validate", response_model=ValidateResponse)
def validate_certificate(code: str = Query(..., alias="code"), db: Session = Depends(get_db)):
    cert = db.query(Certificate).filter(
        Certificate.unique_code == code).first()
    if not cert:
        return ValidateResponse(
            unique_code=code,
            is_valid=False,
            message="Certificate not found"
        )
    '''
    if not cert.signature or not cert.verify_signature():
        return ValidateResponse(
            unique_code=code,
            is_valid=False,
            message="Invalid certificate signature"
        )
    '''

    return ValidateResponse(
        unique_code=code,
        is_valid=True,
        message="Certificate is valid",
        student_name=cert.student.full_name,
        student_email=cert.student.email,
        course_name=cert.course.name,
        issue_date=cert.issue_date,
        expiry_date=cert.expiry_date,
        status=cert.status
    )
