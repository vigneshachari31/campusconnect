from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import SupportTicket, User, Notification
from ..schemas.schemas import SupportCreate, SupportOut
from ..dependencies import require_student, require_admin

router=APIRouter(prefix="/support",tags=["support"])

def out(t):
    return SupportOut(id=t.id,ticket_code=t.ticket_code,subject=t.subject,category=t.category,description=t.description,priority=t.priority,status=t.status,response=t.response,created_at=t.created_at,updated_at=t.updated_at,user_name=t.user.full_name if t.user else None,user_email=t.user.email if t.user else None)

@router.post("",response_model=SupportOut)
def create_ticket(payload:SupportCreate,user:User=Depends(require_student),db:Session=Depends(get_db)):
    code="CC-"+uuid4().hex[:7].upper()
    t=SupportTicket(ticket_code=code,user_id=user.id,**payload.model_dump())
    db.add(t); db.add(Notification(user_id=user.id,message=f"Support request {code} was submitted successfully.")); db.commit(); db.refresh(t); return out(t)

@router.get("/my-tickets",response_model=list[SupportOut])
def my_tickets(user:User=Depends(require_student),db:Session=Depends(get_db)):
    return [out(t) for t in db.query(SupportTicket).filter_by(user_id=user.id).order_by(SupportTicket.created_at.desc()).all()]

@router.get("/{ticket_id}",response_model=SupportOut)
def get_ticket(ticket_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    t=db.get(SupportTicket,ticket_id)
    if not t or t.user_id!=user.id: raise HTTPException(404,"Ticket not found")
    return out(t)
