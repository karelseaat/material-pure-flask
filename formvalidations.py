from wtforms import Form, BooleanField, IntegerField, StringField, PasswordField, validators
from wtforms.widgets import TextArea

class DeviceForm(Form):
    id = IntegerField('id', default=0)
    name = StringField('name', [validators.Length(min=4, max=25)])
    mac = StringField('mac', [validators.Length(min=6, max=35)])

class LoginForm(Form):
    email = StringField('e-mail', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.Length(min=4, max=25)])


class ProfileForm(Form):
    first_name = StringField('First name', [validators.Length(min=4, max=25)])
    sur_name = StringField('Sur name', [validators.Length(min=6, max=35)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    website = StringField('Website', [validators.Length(min=6, max=35)], widget=TextArea())
    AboutMe = StringField('About me', [validators.Length(min=6, max=35)])


class MessageForm(Form):
    recipient = StringField('recipient', [validators.Length(min=4, max=25)])
    title = StringField('title', [validators.Length(min=6, max=35)])
    Message = StringField('Message', [validators.Length(min=6, max=35)], widget=TextArea())



class SignUpForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    password = StringField('password', [validators.Length(min=6, max=35)])
    email = StringField('e-mail', [validators.Length(min=4, max=25)])
    checkbox = StringField('checkbox-1', [validators.Length(min=6, max=35)])


class ForgotForm(Form):
    email = StringField('e-mail', [validators.Length(min=4, max=25)])
