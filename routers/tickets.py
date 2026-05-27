from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional, List
 
from database import get_db
from models import Ticket, Note
from schemas import (
    TicketCreate, TicketUpdate, TicketEdit,
    TicketResponse, TicketDetailResponse,
    TicketCreateResponse, UpdateResponse, DeleteResponse
)
 
router = APIRouter(prefix="/api/tickets", tags=["tickets"])
 
 
def generate_ticket_id(db: Session) -> str:
   
    count = db.query(Ticket).count()
    return f"TKT-{str(count + 1).zfill(3)}"
 
 
def build_ticket_response(t: Ticket) -> TicketResponse:
    
    return TicketResponse(
        id=str(t.id),
        ticket_id=t.ticket_id,
        customer_name=t.customer_name,
        customer_email=t.customer_email,
        subject=t.subject,
        status=t.status,
        priority=t.priority,
        created_at=t.created_at,
        updated_at=t.updated_at
    )
 
 
#CREATE TICKET
 
@router.post("/", response_model=TicketCreateResponse, status_code=201)
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):

    ticket_id = generate_ticket_id(db)
 
    new_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket_data.customer_name.strip(),
        customer_email=ticket_data.customer_email.strip().lower(),
        subject=ticket_data.subject.strip(),
        description=ticket_data.description.strip(),
        status="Open",
        priority=ticket_data.priority.value if ticket_data.priority else "Medium"
    )
 
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
 
    return TicketCreateResponse(
        ticket_id=new_ticket.ticket_id,
        created_at=new_ticket.created_at
    )
 
 
#LIST ALL TICKETS 
 
@router.get("/", response_model=List[TicketResponse])
def list_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Ticket)
 
    if status:
        query = query.filter(Ticket.status == status)
 
    if priority:
        query = query.filter(Ticket.priority == priority)
 
    if search:
        term = f"%{search}%"
        query = query.filter(or_(
            Ticket.customer_name.ilike(term),
            Ticket.customer_email.ilike(term),
            Ticket.subject.ilike(term),
            Ticket.ticket_id.ilike(term),
            Ticket.description.ilike(term)
        ))
 
    tickets = query.order_by(Ticket.created_at.desc()).all()
    return [build_ticket_response(t) for t in tickets]
 
 
#GET SINGLE TICKET
 
@router.get("/{ticket_id}", response_model=TicketDetailResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    """Returns full detail of one ticket including all notes."""
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
 
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
 
    notes = [
        {"id": str(n.id), "note_text": n.note_text, "created_at": n.created_at}
        for n in ticket.notes
    ]
 
    return TicketDetailResponse(
        id=str(ticket.id),
        ticket_id=ticket.ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        notes=notes
    )
 
 
#UPDATE STATUS / ADD NOTE
@router.put("/{ticket_id}", response_model=UpdateResponse)
def update_ticket(ticket_id: str, update_data: TicketUpdate, db: Session = Depends(get_db)):
    """Updates a ticket's status and/or adds a new note."""
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
 
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
 
    if update_data.status:
        ticket.status = update_data.status.value
 
    if update_data.note and update_data.note.strip():
        new_note = Note(ticket_id=ticket.id, note_text=update_data.note.strip())
        db.add(new_note)
 
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
 
    return UpdateResponse(success=True, updated_at=ticket.updated_at)
 
 
#EDIT TICKET DETAILS 
 
@router.patch("/{ticket_id}", response_model=UpdateResponse)
def edit_ticket(ticket_id: str, edit_data: TicketEdit, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
 
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
 
    # Only update fields that were actually sent (not None)
    if edit_data.customer_name is not None:
        ticket.customer_name = edit_data.customer_name.strip()
 
    if edit_data.customer_email is not None:
        ticket.customer_email = edit_data.customer_email.strip().lower()
 
    if edit_data.subject is not None:
        ticket.subject = edit_data.subject.strip()
 
    if edit_data.description is not None:
        ticket.description = edit_data.description.strip()
 
    if edit_data.priority is not None:
        ticket.priority = edit_data.priority.value
 
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
 
    return UpdateResponse(success=True, updated_at=ticket.updated_at)
 
 
#DELETE TICKET
 
@router.delete("/{ticket_id}", response_model=DeleteResponse)
def delete_ticket(ticket_id: str, db: Session = Depends(get_db)):

    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
 
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
 
    db.delete(ticket)
    db.commit()
 
    return DeleteResponse(success=True, message=f"Ticket {ticket_id} deleted successfully")