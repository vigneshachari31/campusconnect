from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import User, EventRegistration, ClubMember, SavedOpportunity, SavedResource
from ..schemas.schemas import UserOut, ProfileUpdate, PasswordUpdate
from ..auth.security import verify_password, hash_password
from ..dependencies import get_current_user

router=APIRouter(prefix="/profile",tags=["profile"])

@router.get("",response_model=UserOut)
def get_profile(user:User=Depends(get_current_user)):
    return user

@router.put("",response_model=UserOut)
def update_profile(payload:ProfileUpdate,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    for k,v in payload.model_dump().items(): setattr(user,k,v)
    db.commit(); db.refresh(user); return user

@router.put("/password")
def change_password(payload:PasswordUpdate,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if not verify_password(payload.current_password,user.password_hash): raise HTTPException(400,"Current password is incorrect")
    user.password_hash=hash_password(payload.new_password); db.commit(); return {"message":"Password changed successfully"}

@router.get("/stats")
def profile_stats(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return {"registered_events":db.query(EventRegistration).filter_by(user_id=user.id).count(),"joined_clubs":db.query(ClubMember).filter_by(user_id=user.id).count(),"saved_opportunities":db.query(SavedOpportunity).filter_by(user_id=user.id).count(),"saved_resources":db.query(SavedResource).filter_by(user_id=user.id).count()}
