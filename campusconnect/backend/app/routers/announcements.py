from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import Announcement, User
from ..schemas.schemas import AnnouncementOut
from ..dependencies import require_admin

router=APIRouter(prefix="/announcements",tags=["announcements"])

@router.get("",response_model=list[AnnouncementOut])
def announcements(db:Session=Depends(get_db)):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).limit(8).all()

@router.post("",response_model=AnnouncementOut)
def create_announcement(title:str,content:str,_:User=Depends(require_admin),db:Session=Depends(get_db)):
    a=Announcement(title=title,content=content); db.add(a); db.commit(); db.refresh(a); return a
