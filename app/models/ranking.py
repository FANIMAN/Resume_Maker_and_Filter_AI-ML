from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.session import Base

class Ranking(Base):
    __tablename__ = "rankings"

    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    score = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=False)
    photo_check = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
