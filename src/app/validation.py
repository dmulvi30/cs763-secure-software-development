from wtforms import Form, StringField, PasswordField, validators

'''
Form for the registration of a new user
'''
class RegistrationForm(Form):
    first_name = StringField('first_name', validators=[
        validators.DataRequired(message='First name should not be empty!')
    ], )
    last_name = StringField('last_name', validators=[
        validators.DataRequired(message='last name should not be empty!')
    ], )
    email = StringField('email', [validators.Email(message="Not an email address")])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.Length(min=8, max=32, message='password must be between 8 and 32 characters long'),

    ])
    confirm_password = PasswordField('confirm_password',
                                     [validators.EqualTo('password', message='The passwords you entered do not match!')])
