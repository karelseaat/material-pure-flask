from flask import Flask, render_template, request
from flask import session as bsession
from flask import Blueprint, redirect, url_for, flash, get_flashed_messages
from models import User, Device, DeviceType
from helpers import pageparameters, historykeep
from dbsession import make_session
import flask_login
from itertools import cycle

from formvalidations import *
from flaskext.markdown import Markdown

from blueprints.auth import auth
from formvalidations import LoginForm
from flask_seasurf import SeaSurf

session = make_session()

login_manager = flask_login.LoginManager()

app = Flask(__name__,
            static_url_path='',
            static_folder = "dist/static",
            template_folder = "dist")

Markdown(app)


login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4q8z\n\xec]/'


csrf = SeaSurf(app)

# print(dir(csrf), csrf)

app.register_blueprint(auth.auth_bp)


@app.errorhandler(401)
def unauthorised(e):
    params = pageparameters()
    # note that we set the 404 status explicitly
    return render_template('401.html.jinja', **params), 404

@app.errorhandler(404)
def notfound(e):
    params = pageparameters()
    # note that we set the 404 status explicitly
    return render_template('404.html.jinja', **params), 404

@flask_login.login_required
def default():
    params = pageparameters()
    return render_template('dashboard.html.jinja', **params)



def index():
    params = pageparameters('InDex')
    return render_template('index.html.jinja', **params)


@flask_login.login_required
def newdevice(id=0):
    params = pageparameters('newdevice')

    if id:
        adevice = session.query(Device).get(id)
        session.close()
        if adevice:
            form = DeviceForm(obj = adevice)
        else:
            form = DeviceForm()
    else:
        form = DeviceForm()

    # form.csrf = app.csrf
    params.update({'submit':'/handle_new_device', 'cancel':url_for('devices')})
    return render_template('deviceform.html.jinja', **params, form = form)

@flask_login.login_required
def handlenewdevice():
    form = DeviceForm(request.form)
    if form.validate():
        print(form.mac.data)
        print(form.name.data)
    else:
        print(form.data)
        print(dir(form), form.errors)

    if form.id.data == 0:
        thedevice = Device(name=form.name.data)
        thedevice.device_type = DeviceType(name="baallala")
    else:
        thedevice = session.query(Device).get(form.id.data)
        thedevice.name = form.name.data
        thedevice.mac = form.mac.data

    session.add(thedevice)


    session.commit()
    session.close()
    return redirect(url_for('devices'))

@flask_login.login_required
def forms():
    params = pageparameters('User Profile')

    if flask_login.current_user.get_id():
        form = ProfileForm(obj = flask_login.current_user)
    else:
        form = ProfileForm()

    params.update({'submit':'/handleprofileform', 'cancel':'/'})
    return render_template('forms.html.jinja', **params, form=form)

@flask_login.login_required
def handleforms():
    return redirect(url_for('default'))


@flask_login.login_required
def devices():
    params = pageparameters('UI Cards')
    params.update({'devices': flask_login.current_user.devices})
    params.update({'add':'/new_device', 'delete':'/delete_device/', 'view':'/view_device/'})
    return render_template('ui-cards.html.jinja', **params)

@flask_login.login_required
def deleteuicard(device_id=0):
    session.query(Device).filter(Device.id == device_id).delete()
    session.commit()
    session.close()
    return redirect(url_for('messagetable'))

def rotate(l, x):
    return l[-x:] + l[:-x]

def nextitem(index, list):
    length = len(list)
    if index >= length:
        return list[0]
    return list[index]

def sortflipper(index, sorts, default_keys=[], default_values=[]):
    index = int(index)
    sorts = sorts.split(',')

    mordefault = ['none'] * len(default_values)
    if index > -1 and sorts:
        possi = default_values.index(sorts[index])
        position = nextitem(possi + 1, default_values)
        sorts[index] = position
        dictionary = dict(zip(default_keys, sorts))
        return ",".join(sorts), dictionary
    else:
        return ",".join(mordefault), dict(zip(default_keys, mordefault))


@flask_login.login_required
def messagetable(index="-1", sorts=""):
    params = pageparameters('UI Tables')
    mega, dictionary = sortflipper(index, sorts,default_keys=['title', 'created', 'user'], default_values=['none', 'ascending','descending' ])
    params.update({'sorts': mega})
    params.update({'keyss': dictionary})

    params.update({'new':'/new_message', 'view':'/view_message/', 'cancel': '/message-tables'})
    return render_template('ui-tables.html.jinja',  **params)

@flask_login.login_required
def newmessage(id=0):
    if id:
        adevice = session.query(Message).get(id)
        session.close()
        if adevice:
            form = MessageForm(obj = adevice)
        else:
            form = MessageForm()
    else:
        form = MessageForm()

    params = pageparameters('New Message')
    params.update({'submit':'/handle_new_message', 'cancel':''})
    return render_template('ui-form-components.html.jinja', **params, form = form)

def termsofservice():
    params = pageparameters('Terms of service')
    return render_template('tos.html.jinja', **params)

@flask_login.login_required
def deletemessage(message_id=0):
    session.query(Message).filter(Device.id == message_id).delete()
    session.commit()
    session.close()
    return redirect(url_for('messagetable'))

@flask_login.login_required
def viewmessage(message_id=0):
    params = pageparameters('View Message')
    params.update({'submit':'/handle_new_message', 'cancel':''})
    return render_template('ui-form-components.html.jinja', **params)

@flask_login.login_required
def handlenewmessage():
    return redirect(url_for('messagetable'))


@login_manager.user_loader
def load_user(user_id):
    try:
        user = session.query(User).get(user_id)
        session.close()
        return user
    except:
        return None


app.add_url_rule('/', view_func=default, methods=['GET'])
app.add_url_rule('/index', view_func=index, methods=['GET'])
app.add_url_rule('/new_device', view_func=newdevice, methods=['GET'])
app.add_url_rule('/new_device/<id>', view_func=newdevice, methods=['GET'])
app.add_url_rule('/handle_new_device', view_func=handlenewdevice, methods=['POST'])
app.add_url_rule('/profileform', view_func=forms, methods=['GET'])
app.add_url_rule('/handleprofileform', view_func=handleforms, methods=['POST'])
app.add_url_rule('/device-cards', view_func=devices, methods=['GET'])
app.add_url_rule('/tos', view_func=termsofservice, methods=['GET'])
app.add_url_rule('/message-tables/<index>/<sorts>', view_func=messagetable, methods=['GET'])
app.add_url_rule('/message-tables', view_func=messagetable, methods=['GET'])
app.add_url_rule('/new_message', view_func=newmessage, methods=['GET'])
app.add_url_rule('/view_message/<message_id>', view_func=viewmessage, methods=['GET'])
app.add_url_rule('/handle_new_message', view_func=handlenewmessage, methods=['POST'])
app.add_url_rule('/delete_message/<message_id>', view_func=deletemessage, methods=['GET'])
app.add_url_rule('/delete_device/<device_id>', view_func=deleteuicard, methods=['GET'])
