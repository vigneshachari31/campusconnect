from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Event, Club, Opportunity, Resource

router=APIRouter(prefix="/search",tags=["search"])

@router.get("")
def global_search(q:str,db:Session=Depends(get_db)):
    term=f"%{q.strip()}%"
    if len(q.strip())<2: return {"query":q,"events":[],"clubs":[],"opportunities":[],"resources":[]}
    events=db.query(Event).filter(or_(Event.title.ilike(term),Event.description.ilike(term),Event.category.ilike(term))).limit(6).all()
    clubs=db.query(Club).filter(or_(Club.name.ilike(term),Club.short_description.ilike(term),Club.category.ilike(term))).limit(6).all()
    opps=db.query(Opportunity).filter(or_(Opportunity.title.ilike(term),Opportunity.organization.ilike(term),Opportunity.description.ilike(term))).limit(6).all()
    resources=db.query(Resource).filter(or_(Resource.title.ilike(term),Resource.description.ilike(term),Resource.category.ilike(term))).limit(6).all()
    return {"query":q,"events":[{"id":e.id,"title":e.title,"type":"event","category":e.category} for e in events],"clubs":[{"id":c.id,"title":c.name,"type":"club","category":c.category} for c in clubs],"opportunities":[{"id":o.id,"title":o.title,"type":"opportunity","category":o.category} for o in opps],"resources":[{"id":r.id,"title":r.title,"type":"resource","category":r.category} for r in resources]}
