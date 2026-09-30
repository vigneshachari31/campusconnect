from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Resource, SavedResource, User, Notification
from ..schemas.schemas import ResourceBase, ResourceOut
from ..dependencies import require_student, require_admin

router=APIRouter(prefix="/resources",tags=["resources"])

def to_out(r,db,user_id=None):
    payload={k:getattr(r,k) for k in ["id","title","category","description","resource_type","url","image_url"]}
    payload["saved"]=bool(user_id and db.query(SavedResource).filter_by(user_id=user_id,resource_id=r.id).first())
    return ResourceOut.model_validate(payload)

@router.get("",response_model=list[ResourceOut])
def list_resources(q:str|None=None,category:str|None=None,db:Session=Depends(get_db)):
    query=db.query(Resource)
    if q: query=query.filter(or_(Resource.title.ilike(f"%{q}%"),Resource.description.ilike(f"%{q}%")))
    if category and category!="All": query=query.filter(Resource.category==category)
    return [to_out(r,db) for r in query.order_by(Resource.title).all()]

@router.get("/saved",response_model=list[ResourceOut])
def saved_resources(user:User=Depends(require_student),db:Session=Depends(get_db)):
    return [to_out(s.resource,db,user.id) for s in db.query(SavedResource).filter_by(user_id=user.id).all()]

@router.get("/{resource_id}",response_model=ResourceOut)
def get_resource(resource_id:int,db:Session=Depends(get_db)):
    r=db.get(Resource,resource_id)
    if not r: raise HTTPException(404,"Resource not found")
    return to_out(r,db)

@router.post("/{resource_id}/save")
def save_resource(resource_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    r=db.get(Resource,resource_id)
    if not r: raise HTTPException(404,"Resource not found")
    if db.query(SavedResource).filter_by(user_id=user.id,resource_id=resource_id).first(): raise HTTPException(409,"Already saved")
    db.add(SavedResource(user_id=user.id,resource_id=resource_id)); db.add(Notification(user_id=user.id,message=f"Saved {r.title} to your resources.")); db.commit(); return {"message":"Resource saved"}

@router.delete("/{resource_id}/save")
def unsave_resource(resource_id:int,user:User=Depends(require_student),db:Session=Depends(get_db)):
    s=db.query(SavedResource).filter_by(user_id=user.id,resource_id=resource_id).first()
    if not s: raise HTTPException(404,"Saved resource not found")
    db.delete(s); db.commit(); return {"message":"Removed from saved resources"}

@router.post("",response_model=ResourceOut)
def create_resource(payload:ResourceBase, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    r=Resource(**payload.model_dump()); db.add(r); db.commit(); db.refresh(r); return to_out(r,db)

@router.put("/{resource_id}",response_model=ResourceOut)
def update_resource(resource_id:int,payload:ResourceBase, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    r=db.get(Resource,resource_id)
    if not r: raise HTTPException(404,"Resource not found")
    for k,v in payload.model_dump().items(): setattr(r,k,v)
    db.commit(); db.refresh(r); return to_out(r,db)

@router.delete("/{resource_id}")
def delete_resource(resource_id:int, _:User=Depends(require_admin),db:Session=Depends(get_db)):
    r=db.get(Resource,resource_id)
    if not r: raise HTTPException(404,"Resource not found")
    db.delete(r); db.commit(); return {"message":"Resource deleted"}
