from flask import Blueprint, redirect, url_for, render_template, request, flash
import flask_login

from helpers import pageparameters
from dbsession import make_session
from models import User
from formvalidations import LoginForm
from flask import current_app

session = make_session()
auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/login')
def login():
    params = pageparameters('Login')
    form = LoginForm()
    params.update({'submit':'/login','signup':'/sign-up','forgot':'/forgot-password'})

    return render_template('login.html.jinja', **params, form=form)


@auth_bp.route('/forgot-password')
def forgot():
    params = pageparameters('Forgot Password')
    params.update({'submit':'/handle-forgot-password', 'cancel':'/login'})

    return render_template('forgot-password.html.jinja', **params)

@auth_bp.route('/handle-forgot-password', methods=['POST'])
def handleforgot():
    return redirect(url_for('login'))

@auth_bp.route('/login', methods=['POST'])
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


# @flask_login.login_required
@auth_bp.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/sign-up')
def signup():
    params = pageparameters('Signup')
    params.update({'submit':'/handle-sign-up', 'already':'/login', 'tos':''})
    return render_template('sign-up.html.jinja', **params)

@auth_bp.route('/handle-sign-up', methods=['POST'])
def handlesignup():
    return redirect(url_for('login'))
