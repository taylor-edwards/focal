import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
  from_email='mailer@focal.pics',
  to_emails='9tedwards@gmail.com',
  subject='Focal Pics Sign-in Link',
  html_content='<h1>Sign into Focal</h1><a href="http://localhost:3000/magic?token=asdf">Sign in</a>'
)

try:
  sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
  response = sg.send(message)
  print(response.status_code)
  print(response.body)
  print(response.headers)
except Exception as err:
  print(err.message)
