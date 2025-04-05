from flask import render_template, redirect, url_for, flash
from app import db
from app.models import Paciente
from app.forms import PacienteForm
from flask import Blueprint

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/registro', methods=['GET', 'POST'])
def registrar_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        paciente = Paciente(
            nombre=form.nombre.data,
            email=form.email.data,
            password=form.password.data,
            identificacion=form.identificacion.data,
            genero=form.genero.data,
            telefono=form.telefono.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            historial_medico=form.historial_medico.data
        )
        db.session.add(paciente)
        db.session.commit()
        flash('Paciente registrado exitosamente!', 'success')
        return redirect(url_for('pacientes.listar'))
    
    return render_template('pacientes/registro.html', form=form)

@pacientes_bp.route('/listar')
def listar():
    pacientes = Paciente.query.all()
    return render_template('pacientes/lista.html', pacientes=pacientes)

__all__ = ['pacientes_bp']