from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Club, ClubMember, User, Notification, Event
from ..schemas.schemas import ClubBase, ClubOut
from ..dependencies import require_student, require_admin, get_current_user

router=APIRouter(prefix="/clubs",tags=["clubs"])

def to_out(c,db):
    payload={k:getattr(c,k) for k in ["id","name","category","logo_url","banner_url","short_description","about","mission","activities","leaders"]}
    payload["member_count"]=db.query(ClubMember).filter_by(club_id=c.id).count()
    return ClubOut.model_validate(payload)

@router.get("",response_model=list[ClubOut])
def list_clubs(q:str|None=None,category:str|None=None,db:Session=Depends(get_db)):
    query=db.query(Club)
    if q: query=query.filter(or_(Club.name.ilike(f"%{q}%"),Club.short_description.ilike(f"%{q}%")))
    if category and category!="All": query=query.filter(Club.category==category)
    return [to_out(c,db) for c in query.order_by(Club.name).all()]

@router.get("/{club_id}",response_model=ClubOut)
def get_club(club_id:int,db:Session=Depends(get_db)):
    c=db.get(Club,club_id)
    if not c: raise HTTPException(404,"Club not found")
    return to_out(c,db)

@router.get("/{club_id}/events")
def club_events(club_id:int,db:Session=Depends(get_db)):
    c=db.get(Club,club_id)
    if not c: raise HTTPException(404,"Club not found")
    return []

@router.post("/{club_id}/join")
def join_club(club_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    c=db.get(Club,club_id)
    if not c: raise HTTPException(404,"Club not found")
    if db.query(ClubMember).filter_by(user_id=user.id,club_id=club_id).first(): raise HTTPException(409,"You already joined this club")
    db.add(ClubMember(user_id=user.id,club_id=club_id)); db.add(Notification(user_id=user.id,message=f"You joined {c.name}.")); db.commit(); return {"message":"Joined ✓"}

@router.delete("/{club_id}/join")
def leave_club(club_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    m=db.query(ClubMember).filter_by(user_id=user.id,club_id=club_id).first()
    if not m: raise HTTPException(404,"Membership not found")
    c=m.club; db.delete(m); db.add(Notification(user_id=user.id,message=f"You left {c.name}.")); db.commit(); return {"message":"You left the club"}

@router.get("/me/joined",response_model=list[ClubOut])
def my_clubs(user:User=Depends(require_student),db:Session=Depends(get_db)):
    return [to_out(m.club,db) for m in db.query(ClubMember).filter_by(user_id=user.id).all()]

@router.post("",response_model=ClubOut)
def create_club(payload:ClubBase, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    c=Club(**payload.model_dump()); db.add(c); db.commit(); db.refresh(c); return to_out(c,db)

@router.put("/{club_id}",response_model=ClubOut)
def update_club(club_id:int,payload:ClubBase, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    c=db.get(Club,club_id)
    if not c: raise HTTPException(404,"Club not found")
    for k,v in payload.model_dump().items(): setattr(c,k,v)
    db.commit(); db.refresh(c); return to_out(c,db)

@router.delete("/{club_id}")
def delete_club(club_id:int, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    c=db.get(Club,club_id)
    if not c: raise HTTPException(404,"Club not found")
    db.delete(c); db.commit(); return {"message":"Club deleted"}

@router.get("/{club_id}/members")
def club_members(club_id:int, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    return [{"id":m.user.id,"name":m.user.full_name,"email":m.user.email} for m in db.query(ClubMember).filter_by(club_id=club_id).all()]
