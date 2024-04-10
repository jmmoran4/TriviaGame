import flask
from flask_login import login_user, login_required, logout_user, UserMixin, LoginManager, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request
import bcrypt
from DB import user_collection
# import flaskr.db, bcrypt, sys
from flaskr.models import User
import html
import DB as db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User(name)
    user_from_db = user_collection.find_one({'username': name})

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user_from_db or not user.check_password(password.encode(), user_from_db.get('password')):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('name')
    name = html.escape(username)
    password = request.form.get('password')
    # hashes and salts the password for storage in the database
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # if this returns None the username doesn't already exist
    user = db.check_for_user(name)
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # adds a new user to the database with the hashed and salted password
    db.add_user(name, hashed_password)

    return redirect(url_for('auth.login'))


@auth.route("/update_profile", methods=['POST'])
@login_required
def update_profile():
    old_pass = request.form.get('oldPassword')
    new_pass = request.form.get('newPassword')

    user = current_user.username
    user_from_db = user_collection.find_one({'username': user})

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not current_user.check_password(old_pass.encode(), user_from_db.get('password')):
        flash('Please check your password and try again.', 'danger')
        return redirect(url_for('main.profile'))  # if the user doesn't exist or password is wrong, reload the page
    else:
        hashed_password = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
        db.update_password(user, hashed_password)
        flash('Password updated successfully!', 'success')
        return redirect(url_for('main.profile'))