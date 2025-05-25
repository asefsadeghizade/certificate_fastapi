import uuid
import hashlib
import json
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Date, DateTime, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = 'certificate_student'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=True, index=True)
    date_of_birth = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    certificates = relationship("Certificate", back_populates="student")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Course(Base):
    __tablename__ = 'certificate_course'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, index=True)
    description = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    certificates = relationship("Certificate", back_populates="course")


class Certificate(Base):
    __tablename__ = 'certificate_certificate'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey(
        'certificate_student.id'), nullable=False)
    course_id = Column(UUID(as_uuid=True), ForeignKey(
        'certificate_course.id'), nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    unique_code = Column(String(50), unique=True, nullable=False, index=True)
    signature = Column(String(64), unique=True, nullable=True)
    status = Column(String(20), nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")

    def generate_signature(self):
        cert_data = {
            'certificate_id': str(self.id),
            'student_id': self.student.student_id,
            'student_name': self.student.full_name,
            'course_name': self.course.name,
            'issue_date': self.issue_date.isoformat(),
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'unique_code': self.unique_code,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        data_string = json.dumps(cert_data, sort_keys=True)
        data_bytes = data_string.encode('utf-8')
        signature = hashlib.sha256(data_bytes).hexdigest()
        return signature

    def verify_signature(self):
        if not self.signature:
            print("Stored signature is missing.")
            return False
        generated = self.generate_signature()
        print("Stored Signature:", self.signature)
        print("Generated Signature:", generated)
        return self.signature == generated
