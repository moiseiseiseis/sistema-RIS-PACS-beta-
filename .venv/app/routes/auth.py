from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return "Página de login"

__all__ = ['auth_bp']