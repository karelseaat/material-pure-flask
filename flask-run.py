from flask import Flask, render_template, request
from flask import session as bsession
from flask import Blueprint, redirect, url_for, flash
from models import User, Device, DeviceType
from dbsession import make_session
import flask_login
from itertools import cycle
from urllib.parse import urlparse, parse_qs
from formvalidations import *
from flaskext.markdown import Markdown



session = make_session()

login_manager = flask_login.LoginManager()

app = Flask(__name__,
            static_url_path='',
            static_folder = "dist/static",
            template_folder = "dist")

Markdown(app)

login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4q8z\n\xec]/'

def historykeep(pagename):
    parsed = urlparse(request.url, '.')
    if 'history' in bsession:
        myses = bsession['history']
        baseurl = "{}://{}{}".format(parsed.scheme, parsed.netloc, parsed.path)
        if not myses or myses[-1:][0][0] != baseurl and pagename:
            myses.append((baseurl, pagename))
        if len(myses) > 6:
            myses = myses[1:]
        bsession['history'] = myses
    else:
        bsession['history'] = []

    return bsession['history'][:-1]

def pageparameters(pagename=None):

    params = {
        'loggedin': bool(flask_login.current_user.get_id()),
        'sitename': 'lolzor',
        'pagename': 'defaultname'
    }

    hist = historykeep(pagename)

    if flask_login.current_user.get_id():
        params.update({
            'history': hist,
            'useremail': flask_login.current_user.email,
            'userimage': flask_login.current_user.profile[0].pic_hash.decode('utf-8'),
            'username': flask_login.current_user.user_name,
            'messages': flask_login.current_user.messages,
            'messagelen': len(flask_login.current_user.messages),
            'profile': flask_login.current_user.profile[0]
        })
    return params

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

def login():
    params = pageparameters('Login')
    params.update({'submit':'/login','signup':'/sign-up','forgot':'/forgot-password'})
    return render_template('login.html.jinja', **params)

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


    # name = request.form.get('name')
    # id = request.form.get('id')

    session.commit()
    session.close()
    return redirect(url_for('devices'))

@flask_login.login_required
def forms():
    params = pageparameters('User Profile')
    params.update({'submit':'/handleprofileform', 'cancel':'/'})
    return render_template('forms.html.jinja', **params)

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
    lels = default_keys
    positions = default_values
    index = int(index)
    sorts = sorts.split(',')

    mordefault = ['none'] * len(default_values)
    if index > -1 and sorts:
        possi = positions.index(sorts[index])
        position = nextitem(possi + 1, positions)
        sorts[index] = position
        dictionary = dict(zip(lels, sorts))
        return ",".join(sorts), dictionary
    else:
        return ",".join(mordefault), dict(zip(lels, mordefault))


@flask_login.login_required
def messagetable(index="-1", sorts=""):
    params = pageparameters('UI Tables')
    mega, dictionary = sortflipper(index, sorts,default_keys=['title', 'created', 'user'], default_values=['none', 'ascending','descending' ])
    params.update({'sorts': mega})
    params.update({'keyss': dictionary})

    params.update({'add':'/new_message', 'view':'/view_message/'})
    return render_template('ui-tables.html.jinja',  **params)

@flask_login.login_required
def newmessage():
    params = pageparameters('New Message')
    params.update({'submit':'/handle_new_message', 'cancel':''})
    return render_template('ui-form-components.html.jinja', **params)

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

def signup():
    params = pageparameters('Signup')
    params.update({'submit':'/handle-sign-up', 'already':'/login', 'tos':''})
    return render_template('sign-up.html.jinja', **params)

def handlesignup():
    return redirect(url_for('login'))

def forgot():
    params = pageparameters('Forgot Password')
    params.update({'submit':'/handle-forgot-password', 'cancel':'/login'})

    return render_template('forgot-password.html.jinja', **params)

@app.route('/handle-forgot-password', methods=['POST'])
def handleforgot():
    return redirect(url_for('login'))

def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = session.query(User).filter(User.email == email).first()
    if user and user.verify_hash(password, user.password_hash):
        flask_login.login_user(user)
    session.close()

    if flask_login.current_user.get_id():
        flash('You were successfully logged in !')
        return redirect(url_for('default'))

    flash('User or password where incorrect !')
    return redirect(url_for('forgot'))

@login_manager.user_loader
def load_user(user_id):
    try:
        user = session.query(User).get(user_id)
        session.close()
        return user
    except:
        return None

@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))


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
app.add_url_rule('/login', view_func=login, methods=['GET'])
app.add_url_rule('/login', view_func=login_post, methods=['POST'])
app.add_url_rule('/sign-up', view_func=signup, methods=['GET'])
app.add_url_rule('/handle-sign-up', view_func=handlesignup, methods=['POST'])
app.add_url_rule('/forgot-password', view_func=forgot, methods=['GET'])
app.add_url_rule('/handle-forgot-password', view_func=handleforgot, methods=['POST'])
app.add_url_rule('/logout', view_func=logout, methods=['GET'])
