# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, getpass



def send_mail(message, owner):
    msg = MIMEMultipart()

    # Configuración de parámetros del mensaje
    msg['From'] = input('Introduzca un usuario gmail: ')
    password = getpass.getpass('Introduzca la contraseña del usuario gmail: ')
    msg['To'] = owner
    msg['Subject'] = 'Challenge MeLi'

    # Agregar en el cuerpo del mensaje
    msg.attach(MIMEText(message, 'plain'))

    # Creación del servidor
    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    # Credenciales de login para enviar el correo
    try:
        server.login(msg['From'], password)
    except:
        print('Usuario y contraseña incorrecta, favor de ejecutar el programa nuevamente')


    # Enviar el mesaje
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()

    print('Mensaje enviado a %s:' % (msg['To']))

