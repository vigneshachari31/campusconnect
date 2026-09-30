from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Notification, User
from ..dependencies import get_current_user

router=APIRouter(prefix="/notifications",tags=["notifications"])

@router.get("")
def list_notifications(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.query(Notification).filter_by(user_id=user.id).order_by(Notification.created_at.desc()).all()
    return [{"id":n.id,"message":n.message,"read":n.read,"created_at":n.created_at} for n in rows]

@router.put("/{notification_id}/read")
def mark_read(notification_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    n=db.get(Notification,notification_id)
    if not n or n.user_id!=user.id: raise HTTPException(404,"Notification not found")
    n.read=True; db.commit(); return {"message":"Marked as read"}

@router.put("/read-all")
def mark_all_read(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    db.query(Notification).filter_by(user_id=user.id,read=False).update({"read":True}); db.commit(); return {"message":"All notifications marked as read"}
