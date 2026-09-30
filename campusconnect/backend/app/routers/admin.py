from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import User, Event, Club, Opportunity, Resource, SupportTicket, EventRegistration
from ..schemas.schemas import SupportOut, SupportUpdate
from ..dependencies import require_admin
from ..routers.support import out as ticket_out

router=APIRouter(prefix="/admin",tags=["admin"])

@router.get("/stats")
def stats(_:User=Depends(require_admin),db:Session=Depends(get_db)):
    return {"students":db.query(User).filter_by(role="student").count(),"events":db.query(Event).count(),"clubs":db.query(Club).count(),"opportunities":db.query(Opportunity).count(),"resources":db.query(Resource).count(),"support_tickets":db.query(SupportTicket).count(),"open_support_requests":db.query(SupportTicket).filter(SupportTicket.status.in_(["Open","In Progress"])).count(),"registrations":db.query(EventRegistration).count()}

@router.get("/students")
def students(q:str|None=None,page:int=Query(1,ge=1),page_size:int=Query(10,ge=1,le=50),_:User=Depends(require_admin),db:Session=Depends(get_db)):
    query=db.query(User).filter(User.role=="student")
    if q: query=query.filter(or_(User.full_name.ilike(f"%{q}%"),User.email.ilike(f"%{q}%"),User.college.ilike(f"%{q}%")))
    total=query.count(); rows=query.order_by(User.created_at.desc()).offset((page-1)*page_size).limit(page_size).all()
    return {"items":[{"id":u.id,"full_name":u.full_name,"email":u.email,"college":u.college,"course":u.course,"year":u.year,"created_at":u.created_at} for u in rows],"total":total,"page":page,"page_size":page_size}

@router.get("/tickets",response_model=list[SupportOut])
def tickets(status:str|None=None,q:str|None=None, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    query=db.query(SupportTicket)
    if status and status!="All": query=query.filter(SupportTicket.status==status)
    if q: query=query.filter(or_(SupportTicket.subject.ilike(f"%{q}%"),SupportTicket.ticket_code.ilike(f"%{q}%")))
    return [ticket_out(t) for t in query.order_by(SupportTicket.created_at.desc()).all()]

@router.put("/tickets/{ticket_id}",response_model=SupportOut)
def update_ticket(ticket_id:int,payload:SupportUpdate,admin:User=Depends(require_admin),db:Session=Depends(get_db)):
    t=db.get(SupportTicket,ticket_id)
    if not t: raise HTTPException(404,"Ticket not found")
    t.status=payload.status; t.response=payload.response; db.add(__import__('builtins').object()) if False else None
    db.add(__import__('__main__').__dict__.get('x')) if False else None
    db.flush()
    from ..models.models import Notification
    db.add(Notification(user_id=t.user_id,message=f"Support request {t.ticket_code} is now {t.status}.")); db.commit(); db.refresh(t); return ticket_out(t)
