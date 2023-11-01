import smtplib
from email.mime.text import MIMEText
import random
from wtforms import Form, StringField, validators

'''
Form for the verification of a new users email
'''
class VerifyCodeForm(Form):
    verifyCode = StringField('verifycode', validators=[
        validators.DataRequired(message='verifycode should not be empty!')
    ], )
    email = StringField('email', [validators.Email(message="Not an email address")])


'''
Sends the email with the verification code
:return: if the email sent successfully
'''
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())
        return True
    except smtplib.SMTPResponseException:
        return False


'''
Generates the verification code for a user registering for the app
:return vercode: the unique verification code for that user
'''
def verification_code():
    num = random.randint(100, 1000)
    capa = chr(random.randint(65, 90))
    capb = chr(random.randint(65, 90))
    low = chr(random.randint(97, 122))
    vercode = capa + str(num) + capb + low
    return vercode
