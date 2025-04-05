from flask import Blueprint

# Crea el Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return "Página principal del sistema RIS"

# Exporta explícitamente el Blueprint
__all__ = ['main_bp']