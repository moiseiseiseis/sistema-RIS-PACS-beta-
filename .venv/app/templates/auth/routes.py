# app/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from app.models import Paciente
from app.forms import RegistroForm, LoginForm
from app.utils import enviar_email_confirmacion
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        user = Paciente(
            nombre=form.nombre.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        
        enviar_email_confirmacion(user)  # ¡Aquí se envía el email!
        
        flash('Se ha enviado un enlace de confirmación a tu email. Por favor verifica tu bandeja.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Paciente.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)  # <-- Así se inicia sesión
            return redirect(url_for('main.index'))
        flash('Email o contraseña incorrectos', 'danger')
    return render_template('auth/login.html', form=form)






@auth.route('/confirmar/<token>')
def confirmar_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = Paciente.query.filter_by(token_confirmacion=token).first()
    if not user or not user.verificar_token(token):
        flash('El enlace de confirmación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))
    
    user.email_confirmado = True
    user.token_confirmacion = None
    db.session.commit()
    
    flash('¡Cuenta confirmada! Ahora puedes iniciar sesión.', 'success')
    return redirect(url_for('auth.login'))