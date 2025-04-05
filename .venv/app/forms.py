from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Optional, Length, ValidationError, EqualTo
from datetime import date
import re

class BaseForm(FlaskForm):
    class Meta:
        locales = ['es_ES', 'es']

def validate_fecha_no_futura(form, field):
    if field.data and field.data > date.today():
        raise ValidationError('La fecha no puede ser futura')

def validate_telefono(form, field):
    if field.data and not re.match(r'^[\d\s\+\-\(\)]{7,20}$', field.data):
        raise ValidationError('Formato de teléfono inválido')

class PacienteForm(BaseForm):
    identificacion = StringField('Identificación')
    nombre = StringField('Nombre Completo', validators=[
        DataRequired(message='El nombre es obligatorio'),
        Length(min=3, max=100)
    ], render_kw={
        "placeholder": "Ej: Juan Pérez López",
        "autofocus": True
    })

    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d',
        validators=[Optional(), validate_fecha_no_futura],
        render_kw={
            "placeholder": "AAAA-MM-DD",
            "pattern": r"\d{4}-\d{2}-\d{2}"  # Raw string corregida
        })


    genero = SelectField('Género', choices=[
        ('', 'Seleccione...'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro/No especificar')
    ], validators=[
        DataRequired(message='Seleccione una opción')
    ])

    telefono = StringField('Teléfono', validators=[
        Optional(),
        validate_telefono
    ], render_kw={
        "placeholder": "Ej: +34 600 123 456"
    })

    email = StringField('Email', validators=[
        DataRequired(message='El email es obligatorio'),
        Email(message='Ingrese un email válido'),
        Length(max=100)
    ], render_kw={
        "placeholder": "Ej: juan.perez@ejemplo.com",
        "type": "email"  # Para validación HTML5
    })

    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es obligatoria'),
        Length(min=8, message='Mínimo 8 caracteres'),
        EqualTo('confirm_password', message='Las contraseñas no coinciden')
    ], render_kw={
        "placeholder": "Mínimo 8 caracteres"
    })

    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Confirme la contraseña')
    ])

    historial_medico = TextAreaField('Historial Médico', validators=[
        Optional(),
        Length(max=2000, message='Máximo 2000 caracteres')
    ], render_kw={
        "placeholder": "Antecedentes médicos relevantes...",
        "rows": 4
    })

    submit = SubmitField('Guardar Paciente', render_kw={
        "class": "btn btn-primary"  # Para integración con Bootstrap
    })

    def validate_identificacion(self, field):
        """Validación personalizada para identificación"""
        if not field.data.isalnum():
            raise ValidationError('Solo caracteres alfanuméricos permitidos')