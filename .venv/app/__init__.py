import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
# Inicialización de extensiones (sin app context)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

def create_app(config_class=Config):
    """Factory principal de la aplicación Flask"""
    app = Flask(__name__)
    
    # 1. Configuración
    app.config.from_object(config_class)
    
    # 2. Asegurar directorio instance
    instance_path = app.instance_path
    Path(instance_path).mkdir(exist_ok=True)
    
    # 3. Inicialización de extensiones
    initialize_extensions(app)
    
    # 4. Registrar blueprints
    register_blueprints(app)
    
    # 5. Configuración adicional
    configure_login_manager(app)
    
    return app

def initialize_extensions(app):
    """Inicializa todas las extensiones Flask"""
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)  # Soporte para SQLite
    login_manager.init_app(app)
    
    # Importar modelos para que Flask-Migrate los detecte
    with app.app_context():
        from app.models import Paciente, Cita

def register_blueprints(app):
    """Registra todos los blueprints de la aplicación"""
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.pacientes import pacientes_bp
    from app.routes import main_bp, auth_bp, pacientes_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(pacientes_bp, url_prefix='/pacientes')

def configure_login_manager(app):
    """Configuración específica para Flask-Login"""
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Cargador de usuario (debe estar aquí para evitar import circular)
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Paciente
        return Paciente.query.get(int(user_id))