# create_db.py
from app import db, create_app

app = create_app()

with app.app_context():
    db.create_all()
    print("¡Tablas creadas exitosamente!")