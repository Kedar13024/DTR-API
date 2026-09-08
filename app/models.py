from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String , text

from .database import Base

class Incident(Base):
    __tablename__ = "incidents"
    incident_id = Column(Integer , primary_key=True , nullable=False)
    type = Column(String, nullable=False)
    description = Column(String , nullable=False)
    severity = Column(String , nullable=False , default="low")
    published = Column(Boolean , nullable=False , default=False)
    reported_at = Column(TIMESTAMP , nullable=False , default=text('now()'))