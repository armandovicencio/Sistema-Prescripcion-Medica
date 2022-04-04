from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_user_mail(request,user):
    subject = 'Correo de Prueba'
    template = get_template('correo.html')

    content = template.render({
        'usuario': user,
        'session_user' : request.session['usuario']
    })

    message = EmailMultiAlternatives(subject, #Titulo
                                    '',
                                    settings.EMAIL_HOST_USER, #Remitente
                                    [user.email]) #Destinatario

    message.attach_alternative(content, 'text/html')

    print(settings.BASE_DIR)

    message.attach_file(settings.BASE_DIR / 'app/static/images/one-piece.jpg')
    message.send()


import threading
from threading import Thread


class EmailThread(threading.Thread):
    def __init__(self, subject, template_correo, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.template_correo = template_correo
        threading.Thread.__init__(self)

    def run (self):
        template = get_template(self.template_correo)

        content = template.render({
            'usuario': 'Francisco',
            'session_user' : 'BOISIER - PRUEBA ASINCRONICA'
        })

        message = EmailMultiAlternatives(self.subject , #Titulo
                                        '',
                                        settings.EMAIL_HOST_USER, #Remitente
                                        self.recipient_list) #Destinatario

        message.attach_alternative(content, 'text/html')

        print(settings.BASE_DIR)

        message.attach_file(settings.BASE_DIR / 'app/static/images/one-piece.jpg')
        message.send()

