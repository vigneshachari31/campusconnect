from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models.models import User, Notification
from ..schemas.schemas import RegisterIn, LoginIn, TokenOut, UserOut
from ..auth.security import hash_password, verify_password, create_access_token
from ..dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(400, "Passwords do not match")
    if db.query(User).filter(User.email == payload.email.lower()).first():
        raise HTTPException(409, "An account with this email already exists")
    user = User(full_name=payload.full_name.strip(), email=payload.email.lower(), password_hash=hash_password(payload.password), college=payload.college.strip(), course=payload.course.strip(), year=payload.year.strip(), role="student")
    db.add(user); db.flush()
    db.add(Notification(user_id=user.id, message="Welcome to CampusConnect! Start exploring events, clubs, and opportunities."))
    db.commit(); db.refresh(user)
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "user": user}

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "user": user}

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
