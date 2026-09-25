"""Pydantic schemas and enums for incident voting."""

from enum import IntEnum

from pydantic import BaseModel


class VoteType(IntEnum):
    """Supported vote values."""

    UPVOTE = 1
    NONE = 0
    DOWNVOTE = -1


class VoteInput(BaseModel):
    """Validate a vote or request to clear a vote."""

    vote_value: VoteType = VoteType.NONE
