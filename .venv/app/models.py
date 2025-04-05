from datetime import datetime, timedelta
import secrets
from enum import Enum
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from flask_login import UserMixin

class TipoEstudio(Enum):
    """Enumeración para tipos de estudios radiológicos (valores cortos para DB)"""
    RX = "RX"
    CT = "CT"
    MRI = "MRI"
    US = "US"
    MAMO = "MAMO"
    PET = "PET"

    @property
    def descripcion(self):
        """Versión legible para el frontend"""
        descriptions = {
            'RX': 'Radiografía',
            'CT': 'Tomografía Computarizada',
            'MRI': 'Resonancia Magnética',
            'US': 'Ultrasonido',
            'MAMO': 'Mamografía',
            'PET': 'Tomografía por Emisión de Positrones'
        }
        return descriptions[self.value]

class EstadoCita(Enum):
    """Estados posibles de una cita"""
    PROGRAMADA = "programada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    EN_PROCESO = "en_proceso"

class Paciente(db.Model, UserMixin):
    """
    Modelo de paciente para el sistema RIS/PACS.
    Incluye autenticación, confirmación por email y relación con citas.
    """
    __tablename__ = 'pacientes'

    # Identificación y datos personales
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    identificacion = db.Column(db.String(20), unique=True, nullable=False, index=True)
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(1), comment="M: Masculino, F: Femenino, O: Otro")
    telefono = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    
    # Autenticación y seguridad
    password_hash = db.Column(db.String(128))
    email_confirmado = db.Column(db.Boolean, default=False)
    token_confirmacion = db.Column(db.String(100))
    token_expiracion = db.Column(db.DateTime)
    
    # Historial y metadata
    historial_medico = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    citas = db.relationship('Cita', backref='paciente', lazy=True, cascade="all, delete-orphan")

    # --- Métodos para Flask-Login ---
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return self.activo
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    # --- Manejo de Tokens ---
    def generar_token_confirmacion(self, expires_in=3600):
        """Genera un token seguro para confirmación de email"""
        self.token_confirmacion = secrets.token_urlsafe(32)
        self.token_expiracion = datetime.utcnow() + timedelta(seconds=expires_in)
        return self.token_confirmacion

    def verificar_token(self, token, max_age=3600):
        """Verifica si el token es válido y no ha expirado"""
        if not self.token_confirmacion or not self.token_expiracion:
            return False
        if datetime.utcnow() > self.token_expiracion:
            return False
        return secrets.compare_digest(self.token_confirmacion, token)
    
    # --- Manejo de Contraseñas ---
    @property
    def password(self):
        raise AttributeError('La contraseña no es un atributo legible')
    
    @password.setter
    def password(self, password):
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Verifica si la contraseña coincide con el hash almacenado"""
        return check_password_hash(self.password_hash, password)

    # --- Propiedades Calculadas ---
    @property
    def edad(self):
        """Calcula la edad del paciente en años"""
        if not self.fecha_nacimiento:
            return None
        hoy = datetime.now().date()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    # --- Métodos de Clase ---
    @classmethod
    def buscar_por_email(cls, email):
        """Busca un paciente por email (case-insensitive)"""
        return cls.query.filter(db.func.lower(cls.email) == db.func.lower(email)).first()

    def __repr__(self):
        return f'<Paciente {self.nombre} ({self.identificacion})>'

# Validador de email
@event.listens_for(Paciente.email, 'set')
def validate_email(target, value, oldvalue, initiator):
    if value and "@" not in value:
        raise ValueError("Formato de email inválido")

class Cita(db.Model):
    """
    Modelo para gestionar citas de estudios radiológicos.
    Relacionado con el modelo Paciente.
    """
    __tablename__ = 'citas'

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    tipo_estudio = db.Column(db.Enum(TipoEstudio), nullable=False)
    estado = db.Column(db.Enum(EstadoCita), default=EstadoCita.PROGRAMADA)
    notas = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # --- Métodos de Instancia ---
    def marcar_como_completada(self):
        """Marca la cita como completada y guarda en DB"""
        self.estado = EstadoCita.COMPLETADA
        db.session.commit()

    def cambiar_estado(self, nuevo_estado):
        """Cambia el estado de la cita validando el valor"""
        if nuevo_estado not in EstadoCita:
            raise ValueError(f"Estado inválido. Opciones: {list(EstadoCita)}")
        self.estado = nuevo_estado
        db.session.commit()

    # --- Métodos de Clase ---
    @classmethod
    def citas_pendientes(cls):
        """Retorna todas las citas no completadas"""
        return cls.query.filter(cls.estado != EstadoCita.COMPLETADA).all()

    def __repr__(self):
        return f'<Cita {self.id} - {self.tipo_estudio.value} ({self.paciente.nombre})>'