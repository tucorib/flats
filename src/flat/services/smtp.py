# -*- coding: utf-8 -*
'''
Created on 1 sept. 2018

@author: tuco
'''
from email.mime.text import MIMEText
import base64

from googleapiclient import errors
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from flat.configuration import smtp

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
APPLICATION_NAME = 'Flats'


def create_service():
    store = file.Storage('../conf/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(smtp.get_smtp_secret(), SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1', http=creds.authorize(Http()))


def send_email(service, ads):
    body = "Nouvelles annonces:\n\n"
    for source, reference, url in ads:
        body += "[%s] %s %s\n" % (source, reference, url)

    message = MIMEText(body)
    message['to'] = smtp.get_smtp_mail()
    message['from'] = smtp.get_smtp_mail()
    message['subject'] = u"[FLATS] Dernières annonces"
    message = {'raw': base64.urlsafe_b64encode(message.as_string())}

    try:
        message = (service.users().messages().send(userId=smtp.get_smtp_mail(), body=message)
                   .execute())
        print 'Message Id: %s' % message['id']
        return message
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
