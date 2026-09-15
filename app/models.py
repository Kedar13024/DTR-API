"""SQLAlchemy ORM models for incidents and users."""
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, UniqueConstraint , text
from sqlalchemy.orm import relationship

from .database import Base

class Incident(Base):
    """Represent an incident reported by a user.

    Attributes:
        incident_id: Primary key of the incident.
        incident_type: Category of the incident.
        description: Details supplied by the reporter.
        severity: Urgency level of the incident.
        published: Whether the incident is publicly visible.
        reported_at: Timestamp when the incident was created.
        reported_by: ID of the user who reported the incident.
        reporter: User relationship for the reporting user.
    """

    __tablename__ = "incidents"
    incident_id = Column(Integer , primary_key=True , nullable=False)
    incident_type = Column(String, nullable=False)
    description = Column(String , nullable=False)
    severity = Column(String , nullable=False , server_default="low")
    published = Column(Boolean , nullable=False , server_default='TRUE')
    reported_at = Column(TIMESTAMP(timezone=True), nullable=False , server_default=text('now()'))
    reported_by = Column(Integer , ForeignKey("users.user_id", ondelete="CASCADE") , nullable=False)

    reporter = relationship("User" , back_populates="incidents")

class User(Base):
    """Represent an application user and their login credentials.

    Attributes:
        user_id: Primary key of the user.
        user_email: Email address used to sign in.
        user_password: Hashed password; never return it in an API response.
        created_at: Timestamp when the user was created.
    """

    __tablename__ = "users"
    user_id = Column(Integer , primary_key=True , nullable=False)
    user_email = Column(String, unique=True , nullable=False)
    user_password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))

    incidents = relationship("Incident", back_populates="reporter")

class Vote(Base):

    __tablename__ = "votes"

    vote_id = Column(Integer , primary_key=True , nullable=False)
    incident_id = Column(Integer , ForeignKey("incidents.incident_id" , ondelete="CASCADE"),nullable=False)
    user_id = Column(Integer ,ForeignKey("users.user_id" , ondelete="CASCADE"),nullable=False)
    vote_value = Column(Integer , nullable=False)

    __table_args__ = (
        UniqueConstraint('incident_id' , 'user_id' , name='unique_user_incident_vote'),
    )
