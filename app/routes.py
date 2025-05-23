from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app.models import Pet, ClinicalHistory, User, Appointment, Client, Service
from app import db
from datetime import datetime
from app.controllers import (
    create_client, create_pet, create_appointment, 
    register_payment, add_clinical_observation, 
    create_user, delete_user, change_user_password
)

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'receptionist':
                return redirect(url_for('main.receptionist_dashboard'))
            elif user.role == 'vet':
                return redirect(url_for('main.vet_dashboard'))
            else:
                flash('Rol no reconocido.')
                return redirect(url_for('main.index'))
        else:
            flash('Usuario o contraseña incorrectos.')
    return render_template('login.html', hide_menu=True)

# Admin dashboard
@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    return render_template('dashboard.html', is_dashboard=True)

# Receptionist dashboard
@bp.route('/reception')
@login_required
def receptionist_dashboard():
    if current_user.role != 'receptionist':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    return render_template('dashboard.html', is_dashboard=True)

# Vet dashboard
@bp.route('/vet')
@login_required
def vet_dashboard():
    if current_user.role != 'vet':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    return render_template('dashboard.html', is_dashboard=True)

@bp.route('/register_client', methods=['GET', 'POST'])
@login_required
def register_client():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        create_client(name, phone, email)
        flash('Cliente registrado exitosamente.')
        return redirect(url_for('main.register_client'))
    return render_template('register_client.html', show_back_menu=True)

@bp.route('/register_pet', methods=['GET', 'POST'])
@login_required
def register_pet():
    if current_user.role not in ['receptionist', 'admin']:
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    clients = Client.query.all()
    if request.method == 'POST':
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']
        age = request.form['age']
        client_id = request.form['client_id']
        create_pet(name, species, breed, age, client_id)
        flash('Mascota registrado exitosamente.')
        return redirect(url_for('main.register_pet'))
    return render_template('register_pet.html', clients=clients, show_back_menu=True)

@bp.route('/schedule_appointment', methods=['GET', 'POST'])
@login_required
def schedule_appointment():
    if request.method == 'POST':
        client_id = request.form['client_id']
        pet_id = request.form['pet_id']
        service_id = request.form['service_id']
        vet_id = request.form['vet_id']
        date_str = request.form['date']
        time_str = request.form['time']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        create_appointment(client_id, pet_id, service_id, vet_id, date, time)
        flash('Cita agendada exitosamente.')
        return redirect(url_for('main.schedule_appointment'))

    clients = Client.query.all()
    pets = Pet.query.all()
    services = Service.query.all()
    vets = User.query.filter_by(role='vet').all()
    return render_template(
        'schedule_appointment.html',
        clients=clients,
        pets=pets,
        services=services,
        vets=vets,
        show_back_menu=True
    )

@bp.route('/payments', methods=['GET', 'POST'])
@login_required
def payments():
    if current_user.role not in ['receptionist', 'admin']:
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    appointments = Appointment.query.all()
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        register_payment(appointment_id)
        flash('Pago resitrado exitosamente.')
        return redirect(url_for('main.payments'))
    return render_template('payments.html', appointments=appointments, show_back_menu=True)

@bp.route('/history')
@login_required
def history():
    return render_template('history.html', show_back_menu=True)

@bp.route('/history/<int:pet_id>')
@login_required
def history_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    histories = ClinicalHistory.query.filter_by(pet_id=pet_id).all()
    return render_template('history.html', pet=pet, histories=histories, show_back_menu=True)

@bp.route('/reports')
@login_required
def reports():
    return render_template('reports.html', show_back_menu=True)

@bp.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('manage_users.html', users=users, show_back_menu=True)

@bp.route('/manage_services')
@login_required
def manage_services():
    return render_template('manage_services.html', show_back_menu=True)

@bp.route('/reset_password/<int:user_id>', methods=['GET', 'POST'])
@login_required
def reset_password(user_id):
    if current_user.role != 'admin':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        new_password = request.form['new_password']
        user.set_password(new_password)
        db.session.commit()
        flash('Contraseña cambiada exitosamente.')
        return redirect(url_for('main.manage_users'))
    return render_template('reset_password.html', user=user, show_back_menu=True)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/create_user', methods=['GET', 'POST'])
@login_required
def create_user_view():
    if current_user.role != 'admin':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        create_user(username, email, role, password)
        flash('Usuario creado exitosamente.')
        return redirect(url_for('main.manage_users'))
    return render_template('create_user.html', show_back_menu=True)

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user_view(user_id):
    if current_user.role != 'admin':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    delete_user(user_id)
    flash('Usuario borrado exitosamente.')
    return redirect(url_for('main.manage_users'))

@bp.route('/appointments_history', methods=['GET', 'POST'])
@login_required
def appointments_history():
    if current_user.role not in ['receptionist', 'admin']:
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    clients = Client.query.all()
    vets = User.query.filter_by(role='vet').all()
    appointments = Appointment.query
    client_id = request.args.get('client_id')
    vet_id = request.args.get('vet_id')
    date = request.args.get('date')
    if client_id:
        appointments = appointments.filter_by(client_id=client_id)
    if vet_id:
        appointments = appointments.filter_by(vet_id=vet_id)
    if date:
        appointments = appointments.filter_by(date=date)
    appointments = appointments.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('appointments_history.html', appointments=appointments, clients=clients, vets=vets, show_back_menu=True)

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current = request.form['current']
        new = request.form['new']
        confirm = request.form['confirm']
        if not current_user.check_password(current):
            flash('La contraseña actual es incorrecta.')
            return redirect(url_for('main.change_password'))
        if new != confirm:
            flash('Las nuevas contraseñas no coinciden.')
            return redirect(url_for('main.change_password'))
        change_user_password(current_user, new)
        flash('Contraseña cambiada exitosamente.')
        return redirect(url_for('main.index'))
    return render_template('change_password.html', show_back_menu=True)

@bp.route('/add_clinical_observation/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def add_clinical_observation_view(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if request.method == 'POST':
        observation = request.form['observation']
        appointment_id = request.form.get('appointment_id')  # Opcional
        add_clinical_observation(pet_id, observation, appointment_id)
        flash('Observacion agregado exitosamente.')
        return redirect(url_for('main.history_pet', pet_id=pet_id))
    return render_template('add_clinical_observation.html', pet=pet, show_back_menu=True)

@bp.route('/my_appointments')
@login_required
def my_appointments():
    if current_user.role != 'vet':
        flash('Acceso denegado.')
        return redirect(url_for('main.index'))
    # Filtra las citas solo del veterinario actual
    appointments = Appointment.query.filter_by(vet_id=current_user.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('my_appointments.html', appointments=appointments, show_back_menu=True)