import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .templates.base import EmailTemplate
import logger

APIKEY = None

try:
    with open('secrets.json') as f:
        r = json.loads(f.read())
        APIKEY = r['apikey']
        logger.info("APIKey was read.")
except Exception as e:
    raise PermissionError("Could not read the API key.", e)


def sendEmail(template: EmailTemplate, email: str, subject: str, fromName = 'Time2Meet Team', fromEmail = 'noreply@yyjlincoln.app', templateOptions: dict = {}, **options) -> bool:
    if APIKEY:
        message = Mail(
            from_email=f'{fromName} <{fromEmail}>',
            to_emails=email,
            subject=subject,
            html_content=template(**templateOptions).Generate(**options))
        try:
            sg = SendGridAPIClient(APIKEY)
            response = sg.send(message)
            return True
        except Exception as e:
            print(e)
            return False
    else:
        raise Exception('A sendgrid API key is required to send emails.')

