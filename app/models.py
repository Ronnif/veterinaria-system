from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """User of the system: admin, receptionist, or vet."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, receptionist, vet

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        """Checks the user's password."""
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    """Client who owns pets and schedules appointments."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    pets = db.relationship('Pet', backref='owner', lazy=True)
    appointments = db.relationship('Appointment', backref='client', lazy=True)

class Pet(db.Model):
    """Pet belonging to a client."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False, index=True)
    histories = db.relationship('ClinicalHistory', backref='pet', lazy=True)
    appointments = db.relationship('Appointment', backref='pet', lazy=True)

class Service(db.Model):
    """Service offered by the clinic."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    appointments = db.relationship('Appointment', backref='service', lazy=True)

class Appointment(db.Model):
    """Appointment between a client, pet, and vet."""
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False, index=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False, index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    vet_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, cancelled, completed
    paid = db.Column(db.Boolean, default=False)
    vet = db.relationship('User', backref='appointments', foreign_keys=[vet_id])
    clinical_histories = db.relationship('ClinicalHistory', backref='appointment', lazy=True)

class ClinicalHistory(db.Model):
    """Clinical history record for a pet, optionally linked to an appointment."""
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False, index=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=True, index=True)  # Can be None
    observations = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return User.query.get(int(user_id))