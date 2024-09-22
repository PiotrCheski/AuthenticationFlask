from flask import Blueprint, render_template, url_for, flash, redirect
from authenticationflask import db, bcrypt
from authenticationflask.users.forms import RegistrationForm, LoginForm
from authenticationflask.models import User
from flask_login import login_user, logout_user

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template("users/register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('logs.logshome'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template("users/login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))