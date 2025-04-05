from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Paciente
from app.forms import PacienteForm
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/pacientes')
def listar_pacientes():
    pacientes = Paciente.query.order_by(Paciente.nombre).all()
    return render_template('pacientes/lista.html', pacientes=pacientes)

@bp.route('/pacientes/registro', methods=['GET', 'POST'])
def registrar_paciente():
    form = PacienteForm()
    
    if form.validate_on_submit():
        paciente = Paciente(
            nombre=form.nombre.data,
            identificacion=form.identificacion.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            genero=form.genero.data,
            telefono=form.telefono.data,
            email=form.email.data,
            historial=form.historial.data
        )
        
        db.session.add(paciente)
        db.session.commit()
        flash('Paciente registrado exitosamente!', 'success')
        return redirect(url_for('main.listar_pacientes'))
    
    return render_template('pacientes/registro.html', form=form)

@bp.route('/pacientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)
    
    if form.validate_on_submit():
        form.populate_obj(paciente)
        db.session.commit()
        flash('Datos del paciente actualizados!', 'success')
        return redirect(url_for('main.listar_pacientes'))
    
    return render_template('pacientes/editar.html', form=form, paciente=paciente)

@bp.route('/pacientes/<int:id>/eliminar', methods=['POST'])
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado correctamente', 'info')
    return redirect(url_for('main.listar_pacientes'))