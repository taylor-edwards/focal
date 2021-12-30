import os
import urllib
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# TODO: limit sends per day to 100 (SendGrid's limited free plan)
# TODO: do not retry sending to failed emails more than X times

ORIGIN = 'http://local.pics:8080' if os.environ.get('FLASK_ENV') == 'development' \
         else 'https://focal.pics'

def sendMessageWithTemplate(to_emails, template_id, data={}):
    message = Mail(
        from_email=('mailer@focal.pics', 'Focal.pics'),
        to_emails=to_emails,
    )
    message.template_id = template_id
    message.dynamic_template_data = data
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    if not (200 <= response.status_code <= 299):
        raise ValueError(f'Message was refused for emails "{to_emails}" '
                         f'(status: {response.status_code})')

def sendSignInMagicLink(email, token):
    if not 1 < email.index('@') < len(email) - 1:
        raise ValueError(f'Email does not appear valid ({email})')
    return sendMessageWithTemplate(
        to_emails=email,
        template_id=os.environ.get('SIGN_IN_SENDGRID_TEMPLATE_ID'),
        data={
            'magic_link': f'{ORIGIN}/magic?token={urllib.parse.quote(token)}'
        }
    )

def sendDeleteAccountMagicLink(email, token):
    if not 1 < email.index('@') < len(email) - 1:
        raise ValueError(f'Email does not appear valid ({email})')
    return sendMessageWithTemplate(
        to_emails=email,
        template_id=os.environ.get('DELETE_ACCOUNT_SENDGRID_TEMPLATE_ID'),
        data={ 'magic_link': f'{ORIGIN}/magic?delete=true&token={urllib.parse.quote(token)}' }
    )

