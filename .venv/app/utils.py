# app/utils.py
from flask import url_for, current_app
from flask_mail import Message
from threading import Thread
from app import mail

def enviar_email_confirmacion(user):
    """Envía un email con enlace para confirmar la cuenta."""
    token = user.generar_token_confirmacion()
    confirm_url = url_for('auth.confirmar_email', token=token, _external=True)
    
    msg = Message(
        subject="Confirma tu Email - RIS/PACS",
        recipients=[user.email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    
    msg.body = f"""¡Gracias por registrarte en nuestro sistema!

Para confirmar tu cuenta, haz clic en el siguiente enlace:
{confirm_url}

Si no solicitaste este registro, ignora este mensaje.

Atentamente,
Equipo MedWave RIS/PACS
"""
    
    # Envío asíncrono (opcional, para no bloquear la app)
    Thread(target=envio_async, args=(current_app._get_current_object(), msg)).start()

def envio_async(app, msg):
    """Envía el email en segundo plano."""
    with app.app_context():
        mail.send(msg)