from datetime import date, timedelta
from sqlalchemy.orm import Session
from .database.database import SessionLocal, engine, Base
from .models.models import User, Event, Club, Opportunity, Resource, Announcement, Notification
from .auth.security import hash_password

IMG = {
    "tech": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
    "hack": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80",
    "photo": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1200&q=80",
    "business": "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80",
    "sports": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80",
    "study": "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?auto=format&fit=crop&w=1200&q=80",
}

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        admin = db.query(User).filter_by(email="admin@campusconnect.com").first()
        student = db.query(User).filter_by(email="student@campusconnect.com").first()
        if not admin:
            admin = User(full_name="CampusConnect Admin", email="admin@campusconnect.com", password_hash=hash_password("Admin@123"), college="CampusConnect University", course="Administration", year="Staff", role="admin")
            db.add(admin)
        if not student:
            student = User(full_name="Alex Student", email="student@campusconnect.com", password_hash=hash_password("Student@123"), college="CampusConnect University", course="Computer Engineering", year="3rd Year", role="student")
            db.add(student)
        db.flush()

        if db.query(Event).count() == 0:
            today = date.today()
            events = [
                Event(title="AI & Machine Learning Workshop", category="Technology", date=today+timedelta(days=4), time="10:00 AM – 1:00 PM", location="Innovation Lab", mode="Offline", image_url=IMG["tech"], description="A hands-on introduction to modern AI concepts, prompt engineering, and practical machine learning workflows.", requirements="Laptop recommended. Open to all departments.", organizer="AI Student Chapter", max_participants=120),
                Event(title="Campus Hackathon 2026", category="Technology", date=today+timedelta(days=10), time="9:00 AM – 9:00 PM", location="Main Auditorium", mode="Offline", image_url=IMG["hack"], description="Build a useful prototype with your team in a one-day campus hackathon featuring mentors and judging rounds.", requirements="Teams of 2–4. Bring a laptop and charger.", organizer="Coding Club", max_participants=300),
                Event(title="Photography Walk", category="Cultural", date=today+timedelta(days=14), time="7:00 AM – 10:00 AM", location="Campus Gate", mode="Offline", image_url=IMG["photo"], description="A guided photo walk exploring campus architecture, candid moments, and street-style compositions.", requirements="Any camera or smartphone.", organizer="Photography Club", max_participants=80),
                Event(title="Entrepreneurship Summit", category="Career", date=today+timedelta(days=18), time="11:00 AM – 4:00 PM", location="Seminar Hall", mode="Offline", image_url=IMG["business"], description="Meet founders, discover early-stage startup stories, and learn about validating ideas, fundraising, and leadership.", requirements="Open to all students.", organizer="Entrepreneurship Club", max_participants=200),
                Event(title="Inter-College Football Tournament", category="Sports", date=today+timedelta(days=24), time="8:00 AM – 5:00 PM", location="University Sports Ground", mode="Offline", image_url=IMG["sports"], description="A full-day inter-college football tournament celebrating competition, teamwork, and campus spirit.", requirements="Registered college teams only.", organizer="Sports Council", max_participants=250),
                Event(title="Resume & Interview Workshop", category="Career", date=today+timedelta(days=7), time="3:00 PM – 5:00 PM", location="Career Center", mode="Online", image_url=IMG["study"], description="Learn how to improve your resume, prepare stories for interviews, and approach entry-level opportunities with confidence.", requirements="Bring your current resume for feedback.", organizer="Career Services", max_participants=150),
            ]
            db.add_all(events)

        if db.query(Club).count() == 0:
            clubs = [
                Club(name="Coding Club", category="Technology", logo_url=IMG["tech"], banner_url=IMG["hack"], short_description="A community for builders, competitive programmers, and curious developers.", about="The Coding Club brings students together to practice problem solving, build products, and learn modern development tools.", mission="Create a culture of learning by building together.", activities="Weekly coding sessions, hackathons, peer mentoring, Git workshops", leaders="Aarav Mehta • Riya Shah"),
                Club(name="Robotics Club", category="Technology", logo_url=IMG["hack"], banner_url=IMG["tech"], short_description="Design, prototype, and compete with robots and embedded systems.", about="An interdisciplinary community exploring robotics, sensors, control, computer vision, and autonomous systems.", mission="Turn engineering ideas into working machines.", activities="Robot builds, electronics labs, competitions, demo days", leaders="Kabir Rao • Sana Khan"),
                Club(name="Photography Club", category="Cultural", logo_url=IMG["photo"], banner_url=IMG["photo"], short_description="Capture campus stories through creative photography.", about="A welcoming space for beginners and enthusiasts to learn visual storytelling and photo editing.", mission="Tell meaningful stories through images.", activities="Photo walks, editing clinics, portfolio reviews, exhibitions", leaders="Meera Joshi • Ishaan Patel"),
                Club(name="Entrepreneurship Club", category="Career", logo_url=IMG["business"], banner_url=IMG["business"], short_description="Turn ideas into experiments, startups, and real-world impact.", about="Students explore entrepreneurship through founder talks, business model practice, and startup experiments.", mission="Make entrepreneurship practical and accessible.", activities="Pitch nights, founder talks, startup sprints, networking", leaders="Ananya Kulkarni • Dev Menon"),
                Club(name="Cultural Club", category="Cultural", logo_url=IMG["photo"], banner_url=IMG["business"], short_description="Celebrate music, art, dance, theatre, and student creativity.", about="The Cultural Club curates events that give students a stage to express themselves and collaborate.", mission="Make campus life more creative and inclusive.", activities="Open mics, festivals, theatre, dance showcases", leaders="Tara Singh • Aditya Nair"),
                Club(name="Sports Club", category="Sports", logo_url=IMG["sports"], banner_url=IMG["sports"], short_description="Stay active, compete hard, and build team spirit.", about="The Sports Club organizes recreational and competitive activities across campus.", mission="Build healthy habits through sport and community.", activities="Tournaments, fitness challenges, practice groups", leaders="Vikram Das • Pooja Patil"),
            ]
            db.add_all(clubs)

        if db.query(Opportunity).count() == 0:
            today = date.today()
            opps = [
                Opportunity(title="Frontend Developer Internship", organization="Nova Labs", category="Internships", location="Remote", deadline=today+timedelta(days=21), description="Build accessible web experiences with React and TypeScript alongside a product engineering team.", skills="React, TypeScript, Git, UI basics", apply_url="https://example.com", image_url=IMG["tech"]),
                Opportunity(title="AI Research Internship", organization="Future Intelligence Lab", category="Internships", location="Hybrid", deadline=today+timedelta(days=28), description="Assist with literature reviews, experiments, and reproducible ML prototypes under mentor guidance.", skills="Python, ML, statistics, research writing", apply_url="https://example.com", image_url=IMG["hack"]),
                Opportunity(title="National Hackathon", organization="BuildNation", category="Hackathons", location="Mumbai", deadline=today+timedelta(days=16), description="Compete in a national product-building challenge focused on technology for social impact.", skills="Problem solving, prototyping, teamwork", apply_url="https://example.com", image_url=IMG["business"]),
                Opportunity(title="Student Innovation Scholarship", organization="Campus Futures Trust", category="Scholarships", location="Online", deadline=today+timedelta(days=35), description="Scholarship support for students with strong academic commitment and community-driven project ideas.", skills="Academic record, project proposal", apply_url="https://example.com", image_url=IMG["study"]),
                Opportunity(title="Startup Workshop", organization="LaunchPad Network", category="Workshops", location="Online", deadline=today+timedelta(days=11), description="A practical workshop on problem validation, customer discovery, and prototyping.", skills="Curiosity, presentation, teamwork", apply_url="https://example.com", image_url=IMG["business"]),
            ]
            db.add_all(opps)

        if db.query(Resource).count() == 0:
            res = [
                Resource(title="Data Structures Notes", category="Study Materials", description="Concise notes covering arrays, linked lists, trees, graphs, hashing, and algorithmic complexity.", resource_type="Notes", url="https://example.com", image_url=IMG["study"]),
                Resource(title="DBMS Previous Year Papers", category="Previous Year Papers", description="A practice pack for relational databases, SQL, normalization, transactions, and indexing.", resource_type="PDF", url="https://example.com", image_url=IMG["study"]),
                Resource(title="Placement Preparation Guide", category="Placement Preparation", description="A structured plan for aptitude, DSA, CS fundamentals, projects, and interview rounds.", resource_type="Guide", url="https://example.com", image_url=IMG["business"]),
                Resource(title="Python Programming Guide", category="Programming", description="Practical Python revision covering syntax, functions, OOP, files, APIs, and common libraries.", resource_type="Guide", url="https://example.com", image_url=IMG["tech"]),
                Resource(title="Interview Questions", category="Interview Preparation", description="Curated technical and behavioral questions with a simple framework for preparing answers.", resource_type="Question Bank", url="https://example.com", image_url=IMG["hack"]),
            ]
            db.add_all(res)

        if db.query(Announcement).count() == 0:
            db.add_all([
                Announcement(title="Campus Hackathon registration is open", content="Teams of 2–4 can now register for the upcoming campus hackathon."),
                Announcement(title="New placement resources added", content="Check the Resources section for updated preparation material."),
                Announcement(title="Club recruitment week starts Monday", content="Explore student communities and join the clubs that match your interests."),
            ])

        if db.query(Notification).count() == 0:
            db.add_all([
                Notification(user_id=student.id, message="Welcome to CampusConnect! Complete your profile to personalize your experience."),
                Notification(user_id=student.id, message="New internship opportunity available: Frontend Developer Internship."),
            ])

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
