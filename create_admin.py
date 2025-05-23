from app import create_app
from app.models import db, User

app = create_app()

with app.app_context():
    username = 'admin'
    email = 'admin@key.com'
    password = 'adminkey'  # Cambia esto por una contraseña segura
    role = 'admin'

    if not User.query.filter_by(username=username).first():
        admin = User(username=username, email=email, role=role)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin user already exists.")