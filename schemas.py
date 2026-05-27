from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum
 
 
class StatusEnum(str, Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"
 
 
class PriorityEnum(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
 
 
#REQUEST schemas
 
class TicketCreate(BaseModel):
    """Shape of data needed to CREATE a new ticket."""
    customer_name: str
    customer_email: str
    subject: str
    description: str
    priority: Optional[PriorityEnum] = PriorityEnum.medium
 
 
class TicketUpdate(BaseModel):
    """
    Shape of data to UPDATE a ticket status/note.
    Both fields are optional.
    """
    status: Optional[StatusEnum] = None
    note: Optional[str] = None
 
 
class TicketEdit(BaseModel):
    """
    Shape of data to EDIT ticket details.
    All fields optional — only send what changed.
    """
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
 
 
#RESPONSE schemas
class NoteResponse(BaseModel):
    """Shape of a note when returned in API responses."""
    id: str
    note_text: str
    created_at: datetime
 
    class Config:
        from_attributes = True
 
 
class TicketResponse(BaseModel):
    """Shape of a ticket in list view — no description or notes to keep it fast."""
    id: str
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
 
    class Config:
        from_attributes = True
 
 
class TicketDetailResponse(BaseModel):
    """Full ticket data including description and all notes."""
    id: str
    ticket_id: str
    customer_name: str
    customer_email: str
    subject: str
    description: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    notes: List[NoteResponse] = []
 
    class Config:
        from_attributes = True
 
 
class TicketCreateResponse(BaseModel):
    """Minimal response after creating a ticket."""
    ticket_id: str
    created_at: datetime
 
 
class UpdateResponse(BaseModel):
    """Response after updating or editing a ticket."""
    success: bool
    updated_at: datetime
 
 
class DeleteResponse(BaseModel):
    """Response after deleting a ticket."""
    success: bool
    message: str