from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models.family import Family
from .models.booking import Booking
from .models.nanny import Nanny
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        nanny = Nanny.query.filter_by(email=email).first()
        family = Family.query.filter_by(email=email).first()

        if nanny:
            if check_password_hash(nanny.password, password):
                flash('Logged in successfully as Nanny!', category='success')
                login_user(nanny, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif family:
            if check_password_hash(family.password, password):
                flash('Logged in successfully as Family!', category='success')
                login_user(family, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.landing_page'))


@auth.route('/signup/family', methods=['GET', 'POST'])
def family_sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        family = Family.query.filter_by(email=email).first()
        if family:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_family = Family(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(
                password1, method='scrypt'))
            new_family.role = 'family'  # Set the role to 'family'
            db.session.add(new_family)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("family_sign_up.html", user=current_user)


@auth.route('/signup/nanny', methods=['GET', 'POST'])
def nanny_sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        nanny = Nanny.query.filter_by(email=email).first()
        if nanny:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_nanny = Nanny(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(
                password1, method='scrypt'))
            new_nanny.role = 'nanny'  # Set the role to 'nanny'
            db.session.add(new_nanny)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("nanny_sign_up.html", user=current_user)
