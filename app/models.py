from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String , text
from .database import Base

class Incident(Base):
    __tablename__ = "incidents"
    incident_id = Column(Integer , primary_key=True , nullable=False)
    incident_type = Column(String, nullable=False)
    description = Column(String , nullable=False)
    severity = Column(String , nullable=False , default="low")
    published = Column(Boolean , nullable=False , server_default='TRUE')
    reported_at = Column(TIMESTAMP(timezone=True), nullable=False , server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer , primary_key=True , nullable=False)
    user_email = Column(String , nullable=False)
    user_password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))