"""Pydantic schemas for API request validation and response serialization."""

from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, ConfigDict, EmailStr

class User(BaseModel):
    """Validate data required to register a user.

    Attributes:
        user_email: User email address.
        user_password: Plain-text password received during registration.
    """

    user_email : EmailStr
    user_password : str

class User_login(BaseModel):
    """Validate a user's login credentials.

    Attributes:
        email: User email address.
        password: Plain-text password.
    """

    email : EmailStr
    password : str

class User_response(BaseModel):
    """Serialize non-sensitive user information in API responses.

    Attributes:
        user_id: Unique user identifier.
        created_at: Timestamp when the user was created.
    """
    
    model_config=ConfigDict(from_attributes = True)

    user_id : int
    created_at : datetime

class VoteType(IntEnum):
    UPVOTE = 1
    NONE = 0
    DOWNVOTE = -1
class Incident_base(BaseModel):
    """Define fields shared by incident request and response schemas.

    Attributes:
        incident_type: Category of the incident.
        description: Reporter-provided incident details.
        severity: Urgency level of the incident.
        published: Whether the incident is visible publicly.
    """

    incident_type : str
    description : str
    severity : str
    published : bool = True

class Incident_create(Incident_base):
    """Validate data used to create an incident."""

class IncidentUpdate(Incident_base):
    """Validate replacement data for an existing incident."""

class IncidentResponse(Incident_base):
    """Serialize an incident and its reporting user.

    Attributes:
        incident_id: Unique incident identifier.
        reported_at: Timestamp when the incident was reported.
        reported_by: ID of the reporting user.
        reporter: Public details of the reporting user.
    """

    model_config=ConfigDict(from_attributes = True)

    incident_id : int
    reported_at : datetime
    reported_by : int
    reporter : User_response
    upvote_count : int
    downvote_count : int

    user_current_voteType : VoteType

class Token_base(BaseModel):
    """Serialize an access token returned after successful login.

    Attributes:
        access_token: Signed JWT used for authenticated requests.
        token_type: Authentication scheme, normally ``bearer``.
    """

    access_token : str
    token_type : str

class Token_data(BaseModel):
    """Represent authenticated user data extracted from a JWT.

    Attributes:
        user_id: Authenticated user's ID, if present in the token.
    """

    user_id : int | None = None


class VoteInput(BaseModel):

    vote_value : VoteType = VoteType.NONE
