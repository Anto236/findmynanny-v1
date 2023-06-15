from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from uuid import uuid4


class Family(db.Model, UserMixin):
    __tablename__ = 'families'
    id = db.Column(db.String(36), primary_key=True, default=str(uuid4()))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    contact_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    preferred_payment_method = db.Column(db.String(200))
    role = db.Column(db.String(50), default='family')

    @property
    def is_nanny(self):
        return False

    @property
    def is_family(self):
        return True
