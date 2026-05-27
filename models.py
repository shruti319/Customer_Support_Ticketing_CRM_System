from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
 
from database import Base
 
 
class Ticket(Base):
    __tablename__ = "tickets"
 
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
 
    ticket_id = Column(String(20), unique=True, nullable=False, index=True)
 
    # Customer info
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(150), nullable=False)
 
    # Ticket content
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
 
    # Status
    status = Column(String(20), nullable=False, default="Open", index=True)
 
    # Priority
    priority = Column(String(10), nullable=False, default="Medium")
 
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
 
    # Relationship
    notes = relationship("Note", back_populates="ticket", cascade="all, delete-orphan")
 
 
class Note(Base):
    __tablename__ = "notes"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
 
    # Foreign key 
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"), nullable=False)
 
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
 
    # Back reference
    ticket = relationship("Ticket", back_populates="notes")
 