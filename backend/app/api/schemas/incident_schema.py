"""Pydantic schemas for incident requests and responses."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.app.api.schemas.user_schema import User_response
from backend.app.api.schemas.vote_schema import VoteType


class IncidentBase(BaseModel):
    """Fields shared by incident creation, update, and response schemas."""

    incident_type: str
    description: str
    severity: str
    published: bool = True


class IncidentCreate(IncidentBase):
    """Validate data used to create an incident."""


class IncidentUpdate(IncidentBase):
    """Validate replacement data for an existing incident."""


class IncidentResponse(IncidentBase):
    """Serialize an incident, its reporter, and vote totals."""

    model_config = ConfigDict(from_attributes=True)

    incident_id: int
    reported_at: datetime
    reported_by: int
    reporter: User_response
    upvote_count: int
    downvote_count: int
    user_current_vote_type: VoteType
