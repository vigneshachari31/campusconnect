from datetime import date, datetime
import re
from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    college: str
    course: str
    year: str
    role: str
    avatar_url: str | None = None

class RegisterIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str
    college: str = Field(min_length=2, max_length=150)
    course: str = Field(min_length=2, max_length=150)
    year: str = Field(min_length=1, max_length=30)
    @field_validator("email")
    @classmethod
    def valid_email(cls, v: str):
        v=v.strip().lower()
        if not EMAIL_RE.match(v): raise ValueError("Invalid email address")
        return v

class LoginIn(BaseModel):
    email: str
    password: str
    @field_validator("email")
    @classmethod
    def normalized_email(cls, v: str): return v.strip().lower()

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ProfileUpdate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    college: str = Field(min_length=2, max_length=150)
    course: str = Field(min_length=2, max_length=150)
    year: str = Field(min_length=1, max_length=30)
    avatar_url: str | None = None

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)

class EventBase(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    category: str
    date: date
    time: str
    location: str
    mode: str = "Offline"
    image_url: str
    description: str
    requirements: str = "Open to all enrolled students."
    organizer: str = "CampusConnect"
    max_participants: int = Field(ge=1, le=100000)

class EventOut(EventBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    registered_participants: int = 0

class ClubBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    category: str
    logo_url: str
    banner_url: str
    short_description: str
    about: str
    mission: str
    activities: str
    leaders: str = "Student Committee"

class ClubOut(ClubBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    member_count: int = 0

class OpportunityBase(BaseModel):
    title: str
    organization: str
    category: str
    location: str
    deadline: date
    description: str
    skills: str
    apply_url: str = "#"
    image_url: str

class OpportunityOut(OpportunityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    saved: bool = False

class ResourceBase(BaseModel):
    title: str
    category: str
    description: str
    resource_type: str = "Guide"
    url: str = "#"
    image_url: str

class ResourceOut(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    saved: bool = False

class SupportCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=220)
    category: str
    description: str = Field(min_length=10, max_length=5000)
    priority: str = "Medium"

class SupportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ticket_code: str
    subject: str
    category: str
    description: str
    priority: str
    status: str
    response: str | None
    created_at: datetime
    updated_at: datetime
    user_name: str | None = None
    user_email: str | None = None

class SupportUpdate(BaseModel):
    status: str
    response: str | None = None

class AnnouncementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    created_at: datetime
