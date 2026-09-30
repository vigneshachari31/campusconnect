from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Opportunity, SavedOpportunity, User, Notification
from ..schemas.schemas import OpportunityBase, OpportunityOut
from ..dependencies import get_current_user, require_student, require_admin

router=APIRouter(prefix="/opportunities",tags=["opportunities"])

def to_out(o,db,user_id=None):
    payload={k:getattr(o,k) for k in ["id","title","organization","category","location","deadline","description","skills","apply_url","image_url"]}
    payload["saved"]=bool(user_id and db.query(SavedOpportunity).filter_by(user_id=user_id,opportunity_id=o.id).first())
    return OpportunityOut.model_validate(payload)

@router.get("",response_model=list[OpportunityOut])
def list_opportunities(q:str|None=None,category:str|None=None,user:User|None=Depends(lambda: None),db:Session=Depends(get_db)):
    query=db.query(Opportunity)
    if q: query=query.filter(or_(Opportunity.title.ilike(f"%{q}%"),Opportunity.organization.ilike(f"%{q}%"),Opportunity.description.ilike(f"%{q}%")))
    if category and category!="All": query=query.filter(Opportunity.category==category)
    return [to_out(o,db,None) for o in query.order_by(Opportunity.deadline).all()]

@router.get("/saved",response_model=list[OpportunityOut])
def saved(user:User=Depends(require_student),db:Session=Depends(get_db)):
    return [to_out(s.opportunity,db,user.id) for s in db.query(SavedOpportunity).filter_by(user_id=user.id).all()]

@router.get("/{opportunity_id}",response_model=OpportunityOut)
def get_opportunity(opportunity_id:int,user:User|None=Depends(lambda: None),db:Session=Depends(get_db)):
    o=db.get(Opportunity,opportunity_id)
    if not o: raise HTTPException(404,"Opportunity not found")
    return to_out(o,db,None)

@router.post("/{opportunity_id}/save")
def save_opportunity(opportunity_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    o=db.get(Opportunity,opportunity_id)
    if not o: raise HTTPException(404,"Opportunity not found")
    if db.query(SavedOpportunity).filter_by(user_id=user.id,opportunity_id=opportunity_id).first(): raise HTTPException(409,"Already saved")
    db.add(SavedOpportunity(user_id=user.id,opportunity_id=opportunity_id)); db.add(Notification(user_id=user.id,message=f"Saved {o.title} to your opportunities.")); db.commit(); return {"message":"Opportunity saved"}

@router.delete("/{opportunity_id}/save")
def unsave_opportunity(opportunity_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    s=db.query(SavedOpportunity).filter_by(user_id=user.id,opportunity_id=opportunity_id).first()
    if not s: raise HTTPException(404,"Saved opportunity not found")
    db.delete(s); db.commit(); return {"message":"Removed from saved opportunities"}

@router.post("",response_model=OpportunityOut)
def create_opportunity(payload:OpportunityBase, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    o=Opportunity(**payload.model_dump()); db.add(o); db.commit(); db.refresh(o); return to_out(o,db)

@router.put("/{opportunity_id}",response_model=OpportunityOut)
def update_opportunity(opportunity_id:int,payload:OpportunityBase, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    o=db.get(Opportunity,opportunity_id)
    if not o: raise HTTPException(404,"Opportunity not found")
    for k,v in payload.model_dump().items(): setattr(o,k,v)
    db.commit(); db.refresh(o); return to_out(o,db)

@router.delete("/{opportunity_id}")
def delete_opportunity(opportunity_id:int, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    o=db.get(Opportunity,opportunity_id)
    if not o: raise HTTPException(404,"Opportunity not found")
    db.delete(o); db.commit(); return {"message":"Opportunity deleted"}
