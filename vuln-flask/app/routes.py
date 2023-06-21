from functools import wraps
from datetime import datetime, timedelta

from flask import Flask
from flask import jsonify
from flask import request, redirect, url_for, flash, render_template, make_response
from flask_login import current_user, login_required, logout_user, login_user
from werkzeug.urls import url_parse

from app import app, db, elasticsearch
from app.models import User
from app.forms import FlagForm, LoginForm, RegistrationForm, ProfileForm


def set_cookie(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        response = f(*args, **kws)
        response = make_response(response)
        if request.cookies.get('access_token') is None:
            response.set_cookie('access_token', value=current_user.get_token(),
                                expires=datetime.now() + timedelta(days=30))
        return response
    return decorated_function


@app.route('/')
@app.route('/index')
@login_required
@set_cookie
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',  title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('access_token')
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    token = request.cookies.get('access_token')
    data = {
        'username': current_user.username,
        'email': current_user.email,
        'bio': current_user.bio
    }
    form = ProfileForm(data=data)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Profile was successfully changed')
        return redirect(url_for('profile'))
    return render_template('profile.html', title='Profile', token=token, form=form)
