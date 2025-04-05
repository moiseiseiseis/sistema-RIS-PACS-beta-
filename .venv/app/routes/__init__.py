# Importa y expone los blueprints
from .main import main_bp
from .auth import auth_bp
from .pacientes import pacientes_bp

__all__ = ['main_bp', 'auth_bp', 'pacientes_bp']