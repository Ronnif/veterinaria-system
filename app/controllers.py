from app.models import db, Client, Pet, Appointment, ClinicalHistory, User
from datetime import date

def create_client(name, phone, email):
    """Create a new client with the given name, phone, and email."""
    new_client = Client(name=name, phone=phone, email=email)
    db.session.add(new_client)
    db.session.commit()
    return new_client

def create_pet(name, species, breed, age, client_id):
    """Create a new pet for a client."""
    new_pet = Pet(name=name, species=species, breed=breed, age=age, client_id=client_id)
    db.session.add(new_pet)
    db.session.commit()
    return new_pet

def create_appointment(client_id, pet_id, service_id, vet_id, date, time):
    """Create a new appointment for a pet with a vet and service."""
    new_appointment = Appointment(
        client_id=client_id,
        pet_id=pet_id,
        service_id=service_id,
        vet_id=vet_id,
        date=date,
        time=time,
        paid=False
    )
    db.session.add(new_appointment)
    db.session.commit()
    return new_appointment

def register_payment(appointment_id):
    """Mark an appointment as paid."""
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.paid = True
    db.session.commit()
    return appointment

def add_clinical_observation(pet_id, observation, appointment_id=None):
    """Add a clinical observation to a pet, optionally linked to an appointment."""
    new_history = ClinicalHistory(
        pet_id=pet_id,
        appointment_id=appointment_id,
        observations=observation,
        date=date.today()
    )
    db.session.add(new_history)
    db.session.commit()
    return new_history

def create_user(username, email, role, password):
    """Create a new user with the given username, email, role, and password."""
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def delete_user(user_id):
    """Delete a user by their ID."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

def change_user_password(user, new_password):
    """Change the password for a given user."""
    user.set_password(new_password)
    db.session.commit()