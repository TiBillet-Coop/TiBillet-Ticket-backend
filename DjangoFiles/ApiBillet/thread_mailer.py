import os
import threading
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
from BaseBillet.models import Configuration, Reservation, Ticket

import logging
logger = logging.getLogger(__name__)


'''
from ApiBillet.thread_mailer import ThreadMaileur
config = Configuration.get_solo()
context = {'config': config, }
mail = ThreadMaileur('jturbeaux@pm.me', "Vos Billets", template='mails/ticket.html', context=context)
mail.send_with_tread()
'''


class ThreadMaileur():

    def __init__(self, email, title, text=None, html=None, template=None, context=None):
        self.title = title
        self.email = email
        self.text = text
        self.html = html
        self.config = Configuration.get_solo()
        self.context = None
        if template and context :
            self.html = render_to_string(template, context=context)
            self.context = context
        self.attached_file = self._attached_file()

    def _attached_file(self):
        attached_file = []
        if self.context :
            if self.context.get('reservation'):
                reservation: Reservation = self.context.get('reservation')
                tickets = reservation.tickets.filter(status=Ticket.NOT_SCANNED)
                if len(tickets) > 0:
                    for ticket in tickets :
                        attached_file.append(render_to_string('ticket/ticket.html', context={'context': 'context'}))
        return attached_file

    def config_valid(self):
        EMAIL_HOST = os.environ.get('EMAIL_HOST')
        EMAIL_PORT = os.environ.get('EMAIL_PORT')
        EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

        if EMAIL_HOST and EMAIL_PORT and EMAIL_HOST_USER and EMAIL_HOST_PASSWORD and self.config.email :
            return True
        else:
            return False

    def send(self):
        if self.html and self.config_valid() :
            logger.info(f'  send_mail')
            mail = EmailMultiAlternatives(
                self.title,
                self.text,
                self.config.email,
                [self.email,],
            )
            mail.attach_alternative(self.html, "text/html")

            # msg = EmailMessage(subject, html_content, from_email, [to])
            # msg.content_subtype = "html"  # Main content is now text/html
            # msg.send()

            # import ipdb; ipdb.set_trace()
            i=1
            for file in self.attached_file:
                html_before_pdf = HTML(string=file)
                mail.attach(f'ticket_{i}.pdf', html_before_pdf.write_pdf(), 'application/pdf')
                i += 1


            mail_return = mail.send(fail_silently=False)
            if mail_return == 1 :
                logger.info(f'      mail envoyé : {mail_return} - {self.email}')
            else :
                logger.error(f'     mail non envoyé : {mail_return} - {self.email}')
            return mail
        else :
            logger.error(f'Pas de contenu HTML ou de configuration email valide')
            raise ValueError('Pas de contenu HTML ou de configuration email valide')


    def send_with_tread(self):

        self.send()
        # logger.info(f'{timezone.now()} on lance le thread email {self.email}')
        # thread_email = threading.Thread(target=self.send)
        # thread_email.start()
        # logger.info(f'{timezone.now()} Thread email lancé')