from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    birth_date = db.Column(db.Date, nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(120))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.first_name, " ", self.last_name)

'''user_loader "callback" function. 
This callback is used to reload the user object from the user ID stored in the session.
It should take the Unicode ID of a user, and return the corresponding user object.'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_title = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Service(db.Model):
    """
    Create a Services table
    """

    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    cost = db.Column(db.String(20))
    appointments = db.relationship('Appointment', backref='service',
                            lazy='dynamic')

    def __repr__(self):
        return '<Service: {}>'.format(self.name)


class Appointment(db.Model):
    """
    Create an Appointments table
    """

    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_start_time = db.Column(db.String(20), nullable=False)
    appointment_end_time = db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    barber_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    def __repr__(self):
        return '<Appointment: {}>'.format(self.customer_id, " ", self.barber_id, " ", self.service_id)