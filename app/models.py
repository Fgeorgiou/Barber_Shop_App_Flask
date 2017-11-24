from app import db
from hashlib import md5

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(64), nullable=False)
    l_name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column('dob', db.Date, nullable=False)
    telephone_num = db.Column('contact_number', db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, first_name, last_name, birth_date, telephone_num, email, password):
        self.f_name = first_name
        self.l_name = last_name
        self.birth_date = birth_date
        self.telephone_num = telephone_num
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.f_name, " ",self.l_name)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3