from flask import render_template, redirect, url_for, flash, abort, request
from app import db
from app.models import Paciente
from app.forms import PacienteForm
from flask import Blueprint
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/registro', methods=['GET', 'POST'])
def registrar_paciente():
    form = PacienteForm()
    if form.validate_on_submit():
        try:
            # Verificación de duplicados
            if Paciente.query.filter_by(email=form.email.data.lower()).first():
                flash('Este email ya está registrado', 'danger')
                return render_template('pacientes/registro.html', form=form)
            
            if Paciente.query.filter_by(identificacion=form.identificacion.data).first():
                flash('Esta identificación ya está registrada', 'danger')
                return render_template('pacientes/registro.html', form=form)

            paciente = Paciente(
                nombre=form.nombre.data.strip(),
                email=form.email.data.lower().strip(),
                password_hash=generate_password_hash(form.password.data),
                identificacion=form.identificacion.data.strip(),
                genero=form.genero.data,
                telefono=form.telefono.data.strip(),
                fecha_nacimiento=form.fecha_nacimiento.data,
                historial_medico=form.historial_medico.data.strip() if form.historial_medico.data else None
            )
            
            db.session.add(paciente)
            db.session.commit()
            flash('Paciente registrado exitosamente!', 'success')
            return redirect(url_for('pacientes.listar'))
            
        except IntegrityError:
            db.session.rollback()
            flash('Error: Datos duplicados o inválidos', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar paciente: {str(e)}', 'danger')
    
    return render_template('pacientes/registro.html', form=form)

@pacientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)
    
    if form.validate_on_submit():
        try:
            # Validar campos inmutables
            if form.email.data.lower() != paciente.email:
                flash('No puedes modificar el email', 'warning')
                return redirect(url_for('pacientes.editar_paciente', id=id))
            
            if form.identificacion.data != paciente.identificacion:
                flash('No puedes modificar la identificación', 'warning')
                return redirect(url_for('pacientes.editar_paciente', id=id))
            
            # Actualizar campos permitidos
            paciente.nombre = form.nombre.data.strip()
            paciente.genero = form.genero.data
            paciente.telefono = form.telefono.data.strip()
            paciente.fecha_nacimiento = form.fecha_nacimiento.data
            paciente.historial_medico = form.historial_medico.data.strip() if form.historial_medico.data else None
            
            db.session.commit()
            flash('Paciente actualizado exitosamente!', 'success')
            return redirect(url_for('pacientes.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar paciente: {str(e)}', 'danger')
    
    return render_template('pacientes/editar.html', form=form, paciente=paciente)

@pacientes_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_paciente(id):
    if request.method == 'POST':
        try:
            paciente = Paciente.query.get_or_404(id)
            db.session.delete(paciente)
            db.session.commit()
            flash('Paciente eliminado exitosamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al eliminar paciente: {str(e)}', 'danger')
    return redirect(url_for('pacientes.listar'))

@pacientes_bp.route('/listar')
def listar():
    try:
        search = request.args.get('search', '').strip()
        query = Paciente.query.order_by(Paciente.nombre.asc())
        
        if search:
            query = query.filter(
                (Paciente.nombre.ilike(f'%{search}%')) |
                (Paciente.identificacion.ilike(f'%{search}%')) |
                (Paciente.email.ilike(f'%{search}%'))
            )
        
        pacientes = query.all()
        return render_template('pacientes/lista.html', pacientes=pacientes, search_term=search)
    except Exception as e:
        flash(f'Error al cargar la lista de pacientes: {str(e)}', 'danger')
        return render_template('pacientes/lista.html', pacientes=[], search_term='')

__all__ = ['pacientes_bp']