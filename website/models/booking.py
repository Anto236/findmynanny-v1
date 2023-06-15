from website import db
from sqlalchemy.sql import func
from uuid import uuid4


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid4()))
    family_id = db.Column(db.String(36), db.ForeignKey('families.id'))
    nanny_id = db.Column(db.String(36), db.ForeignKey('nannies.id'))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    job_description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=func.now())
    
    family = db.relationship('Family', backref=db.backref('bookings', lazy=True))
    nanny = db.relationship('Nanny', backref=db.backref('bookings', lazy=True))
