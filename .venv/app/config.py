import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuración de Flask
    FLASK_APP = 'run.py'
    FLASK_ENV = 'development'
    
    # Configuración de base de datos
    BASE_DIR = Path(__file__).parent
    DB_DIR = BASE_DIR / 'instance'
    DB_PATH = DB_DIR / 'ris.db'  # Usa minúsculas consistentemente
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'ris.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'tu-clave-secreta-aqui'  # Cambia esto en producción!
    
    # Configuración de email (solo una versión)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tu_email@gmail.com'  # Usa variables de entorno en producción
    MAIL_PASSWORD = 'tu_contraseña'       # Nunca hardcodear en producción
    MAIL_DEFAULT_SENDER = 'tu_email@gmail.com'

    @classmethod
    def init_db_dir(cls):
        """Crea el directorio de la base de datos si no existe"""
        cls.DB_DIR.mkdir(exist_ok=True)