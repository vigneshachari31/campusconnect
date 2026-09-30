from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, Date, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    college: Mapped[str] = mapped_column(String(150), default="CampusConnect University")
    course: Mapped[str] = mapped_column(String(150), default="Computer Engineering")
    year: Mapped[str] = mapped_column(String(30), default="3rd Year")
    role: Mapped[str] = mapped_column(String(20), default="student", index=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    category: Mapped[str] = mapped_column(String(60), index=True)
    date: Mapped[date] = mapped_column(Date)
    time: Mapped[str] = mapped_column(String(50))
    location: Mapped[str] = mapped_column(String(200))
    mode: Mapped[str] = mapped_column(String(30), default="Offline")
    image_url: Mapped[str] = mapped_column(String(700))
    description: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str] = mapped_column(Text, default="Open to all enrolled students.")
    organizer: Mapped[str] = mapped_column(String(150), default="CampusConnect")
    max_participants: Mapped[int] = mapped_column(Integer, default=100)
    registrations: Mapped[list["EventRegistration"]] = relationship(back_populates="event", cascade="all, delete-orphan")

class EventRegistration(Base):
    __tablename__ = "event_registrations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship()
    event: Mapped[Event] = relationship(back_populates="registrations")

class Club(Base):
    __tablename__ = "clubs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    category: Mapped[str] = mapped_column(String(60), index=True)
    logo_url: Mapped[str] = mapped_column(String(700))
    banner_url: Mapped[str] = mapped_column(String(700))
    short_description: Mapped[str] = mapped_column(Text)
    about: Mapped[str] = mapped_column(Text)
    mission: Mapped[str] = mapped_column(Text)
    activities: Mapped[str] = mapped_column(Text)
    leaders: Mapped[str] = mapped_column(String(300), default="Student Committee")
    members: Mapped[list["ClubMember"]] = relationship(back_populates="club", cascade="all, delete-orphan")

class ClubMember(Base):
    __tablename__ = "club_members"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    club_id: Mapped[int] = mapped_column(ForeignKey("clubs.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship()
    club: Mapped[Club] = relationship(back_populates="members")

class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(220), index=True)
    organization: Mapped[str] = mapped_column(String(180))
    category: Mapped[str] = mapped_column(String(60), index=True)
    location: Mapped[str] = mapped_column(String(150))
    deadline: Mapped[date] = mapped_column(Date)
    description: Mapped[str] = mapped_column(Text)
    skills: Mapped[str] = mapped_column(String(400), default="Communication, teamwork")
    apply_url: Mapped[str] = mapped_column(String(700), default="#")
    image_url: Mapped[str] = mapped_column(String(700))
    saved: Mapped[list["SavedOpportunity"]] = relationship(back_populates="opportunity", cascade="all, delete-orphan")

class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship()
    opportunity: Mapped[Opportunity] = relationship(back_populates="saved")

class Resource(Base):
    __tablename__ = "resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(220), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(Text)
    resource_type: Mapped[str] = mapped_column(String(40), default="Guide")
    url: Mapped[str] = mapped_column(String(700), default="#")
    image_url: Mapped[str] = mapped_column(String(700))
    saved: Mapped[list["SavedResource"]] = relationship(back_populates="resource", cascade="all, delete-orphan")

class SavedResource(Base):
    __tablename__ = "saved_resources"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship()
    resource: Mapped[Resource] = relationship(back_populates="saved")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    subject: Mapped[str] = mapped_column(String(220))
    category: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(30), default="Medium")
    status: Mapped[str] = mapped_column(String(30), default="Open")
    response: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user: Mapped[User] = relationship()

class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(String(500))
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship()

class Announcement(Base):
    __tablename__ = "announcements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(220))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
