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
CHUNKSIZE = 50


def create_service():
    store = file.Storage('../conf/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(smtp.get_smtp_secret(), SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1', http=creds.authorize(Http()), cache_discovery=False)


def send_email(service, ads):
    for c in range(0, len(ads), CHUNKSIZE):
        body = "Nouvelles annonces:<br/><br/>"
        for source, reference, url in ads[c:c + CHUNKSIZE]:
            body += "[%s] <a href='%s'>%s</a><br/>" % (source, url, reference)

        message = MIMEText(body, 'html')
        message['to'] = smtp.get_smtp_mail()
        message['from'] = smtp.get_smtp_mail()
        message['subject'] = u"[FLATS] Dernières annonces"
        message = {'raw': base64.urlsafe_b64encode(message.as_string())}

        try:
            service.users().messages().send(userId=smtp.get_smtp_mail(), body=message).execute()
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
