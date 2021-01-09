from flask import Flask, render_template, request
from flask import Blueprint, redirect, url_for, flash

from models import User
from dbsession import make_session
import flask_login

session = make_session()

login_manager = flask_login.LoginManager()

app = Flask(__name__,
            static_url_path='',
            static_folder = "dist/static",
            template_folder = "dist")

login_manager.init_app(app)
app.secret_key = b'_5#y2L"F4q8z\n\xec]/'

def everytime():

    params = {
        'loggedin': bool(flask_login.current_user.get_id()),
    }

    # print(flask_login.current_user.get_id())

    if flask_login.current_user.get_id():
        params.update({
            'useremail': flask_login.current_user.email,
            'userimage': flask_login.current_user.profile[0].pic_hash.decode('utf-8'),
            'username': flask_login.current_user.user_name,
            'messages': flask_login.current_user.messages,
            'messagelen': len(flask_login.current_user.messages),
            'profile': flask_login.current_user.profile[0]
        })


    return params

@app.errorhandler(404)
def page_not_found(e):
    params = everytime()
    # note that we set the 404 status explicitly
    return render_template('404.html.jinja', params = params), 404

@app.errorhandler(401)
def unauthorised(e):
    params = everytime()
    # note that we set the 404 status explicitly
    return render_template('404.html.jinja', params = params), 404

@app.route('/')
@flask_login.login_required
def default():
    params = everytime()
    print(params)
    return render_template('dashboard.html.jinja', params = params)

@app.route('/index')
def index():
    params = everytime()
    return render_template('index.html.jinja', params = params)


@app.route('/charts')
@flask_login.login_required
def charts():
    params = everytime()
    return render_template('charts.html.jinja', params = params)

@app.route('/new_device')
@flask_login.login_required
def newdevice():
    params = everytime()
    return render_template('deviceform.html.jinja', params = params)

@app.route('/handle_new_device')
@flask_login.login_required
def handlenewdevice():
    return redirect(url_for('ui-cards'))


@app.route('/profileform')
@flask_login.login_required
def forms():
    params = everytime()
    return render_template('forms.html.jinja', params = params)

@app.route('/ui-buttons')
def uibuttons():
    params = everytime()
    return render_template('ui-buttons.html.jinja', params = params)

@app.route('/ui-cards')
@flask_login.login_required
def uicards():
    params = everytime()
    params.update({'devices': flask_login.current_user.devices})
    return render_template('ui-cards.html.jinja', params = params)

@app.route('/ui-colors')
def uicolors():
    params = everytime()
    return render_template('ui-colors.html.jinja', params = params)

@app.route('/ui-components')
def uicomponents():
    params = everytime()
    return render_template('ui-components.html.jinja', params = params)

@app.route('/ui-icons')
def uiicons():
    params = everytime()
    return render_template('ui-icons.html.jinja', params = params)

@app.route('/ui-list-components')
def uilistcomponents():
    params = everytime()
    return render_template('ui-list-components.html.jinja', params = params)

@app.route('/ui-tables')
@flask_login.login_required
def uitables():
    params = everytime()
    return render_template('ui-tables.html.jinja', params = params)

@app.route('/new_message')
@flask_login.login_required
def newmessage():
    params = everytime()
    return render_template('ui-form-components.html.jinja', params = params)

@app.route('/view_message')
@flask_login.login_required
def viewmessage():
    params = everytime()
    return render_template('ui-form-components.html.jinja', params = params)

@app.route('/handle_new_message')
@flask_login.login_required
def handlenewmessage():
    return redirect(url_for('uitables'))

@app.route('/delete_message')
@flask_login.login_required
def deletemessage():
    return redirect(url_for('uitables'))

@app.route('/delete_device')
@flask_login.login_required
def deletedevice():
    return redirect(url_for('uicards'))


@app.route('/ui-typography')
def uitypography():
    params = everytime()
    return render_template('ui-typography.html.jinja', params = params)

@app.route('/login')
def login():
    params = everytime()
    return render_template('login.html.jinja', params = params)

@app.route('/sign-up')
def signup():
    params = everytime()
    return render_template('sign-up.html.jinja', params = params)

@app.route('/forgot-password')
def forgot():
    params = everytime()
    return render_template('forgot-password.html.jinja', params = params)


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = session.query(User).filter(User.email == email).first()
    if user and user.verify_hash(password, user.password_hash):
        flask_login.login_user(user)
    session.close()

    if flask_login.current_user.get_id():
        return redirect(url_for('default'))

    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    try:
        user = session.query(User).get(user_id)
        session.close()
        return user
    except:
        return None

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))
