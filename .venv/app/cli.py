from app import create_app, db
from app.models import Paciente, Cita  # Asegúrate de importar todos los modelos

app = create_app()

@app.cli.command('init-db')
def init_db():
    """Inicializa la base de datos"""
    with app.app_context():
        db.create_all()
    print("Base de datos creada correctamente en:", app.instance_path)