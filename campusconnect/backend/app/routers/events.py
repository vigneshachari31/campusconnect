from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Event, EventRegistration, User, Notification
from ..schemas.schemas import EventBase, EventOut
from ..dependencies import get_current_user, require_admin, require_student

router = APIRouter(prefix="/events", tags=["events"])

def to_out(e, db):
    payload={k:getattr(e,k) for k in ["id","title","category","date","time","location","mode","image_url","description","requirements","organizer","max_participants"]}
    payload["registered_participants"]=db.query(EventRegistration).filter_by(event_id=e.id).count()
    return EventOut.model_validate(payload)

@router.get("", response_model=list[EventOut])
def list_events(q: str | None = None, category: str | None = None, mode: str | None = None, upcoming: bool = True, db: Session = Depends(get_db)):
    query = db.query(Event)
    if q: query = query.filter(or_(Event.title.ilike(f"%{q}%"), Event.description.ilike(f"%{q}%"), Event.location.ilike(f"%{q}%")))
    if category and category != "All": query = query.filter(Event.category == category)
    if mode and mode != "All": query = query.filter(Event.mode == mode)
    if upcoming: query = query.filter(Event.date >= date.today())
    query = query.order_by(Event.date.asc())
    return [to_out(e, db) for e in query.all()]

@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    e = db.get(Event, event_id)
    if not e: raise HTTPException(404, "Event not found")
    return to_out(e, db)

@router.post("", response_model=EventOut)
def create_event(payload: EventBase, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    e = Event(**payload.model_dump()); db.add(e); db.commit(); db.refresh(e); return to_out(e, db)

@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, payload: EventBase, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    e = db.get(Event, event_id)
    if not e: raise HTTPException(404, "Event not found")
    for k,v in payload.model_dump().items(): setattr(e,k,v)
    db.commit(); db.refresh(e); return to_out(e, db)

@router.delete("/{event_id}")
def delete_event(event_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    e = db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    db.delete(e); db.commit(); return {"message":"Event deleted"}


@router.get("/{event_id}/registrations")
def event_registrations(event_id:int, _:User=Depends(require_admin), db:Session=Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    return [{"id":r.user.id,"full_name":r.user.full_name,"email":r.user.email,"registered_at":r.created_at} for r in db.query(EventRegistration).filter_by(event_id=event_id).all()]

@router.post("/{event_id}/register")
def register_event(event_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    e=db.get(Event,event_id)
    if not e: raise HTTPException(404,"Event not found")
    if db.query(EventRegistration).filter_by(user_id=user.id,event_id=event_id).first(): raise HTTPException(409,"You are already registered")
    count=db.query(EventRegistration).filter_by(event_id=event_id).count()
    if count >= e.max_participants: raise HTTPException(400,"This event is full")
    db.add(EventRegistration(user_id=user.id,event_id=event_id)); db.add(Notification(user_id=user.id,message=f"You're registered for {e.title}.")); db.commit()
    return {"message":"You're registered!"}

@router.delete("/{event_id}/register")
def cancel_registration(event_id: int, user: User = Depends(require_student), db: Session = Depends(get_db)):
    reg=db.query(EventRegistration).filter_by(user_id=user.id,event_id=event_id).first()
    if not reg: raise HTTPException(404,"Registration not found")
    e=reg.event; db.delete(reg); db.add(Notification(user_id=user.id,message=f"Your registration for {e.title} was cancelled.")); db.commit(); return {"message":"Registration cancelled"}

@router.get("/me/registered", response_model=list[EventOut])
def my_events(user: User = Depends(require_student), db: Session = Depends(get_db)):
    regs=db.query(EventRegistration).filter_by(user_id=user.id).all()
    return [to_out(r.event,db) for r in regs]
