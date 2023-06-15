from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
from . import db
from .models.family import Family
from .models.nanny import Nanny
from .models.booking import Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


views = Blueprint('views', __name__)


@views.route('/')
def landing_page():
    return render_template('landing_page.html')


@views.route('/nanny_dashboard')
@login_required
def nanny_dashboard():
    # Logic for the nanny dashboard
    return render_template('nanny_dashboard.html')


@views.route('/family_dashboard')
@login_required
def family_dashboard():
    # Logic for the family dashboard
    return render_template('family_dashboard.html')


@views.route('/home')
@login_required
def home():
    if current_user.is_family:
        return redirect(url_for("views.family_dashboard"))
    elif current_user.is_nanny:
        return redirect(url_for("views.nanny_dashboard"))
    else:
        return redirect(url_for("auth.logout"))


@views.route('/nanny/profile', methods=['GET', 'POST'])
@login_required
def update_nanny_profile():
    nanny = current_user

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        hourly_rate = request.form.get('hourly_rate')
        years_of_experience = request.form.get('years_of_experience')
        city = request.form.get('city')

        if email:
            existing_nanny = Nanny.query.filter_by(email=email).first()
            if existing_nanny and existing_nanny != nanny:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                nanny.email = email

        if first_name:
            if len(first_name) < 2:
                flash('First Name must be greater than 1 character.',
                      category='error')
            else:
                nanny.first_name = first_name

        if last_name:
            if len(last_name) < 2:
                flash('Last Name must be greater than 1 character.',
                      category='error')
            else:
                nanny.last_name = last_name

        if password1 and password1 == password2:
            if len(password1) < 7:
                flash('Password must be greater than 7 characters.',
                      category='error')
            else:
                nanny.password = generate_password_hash(
                    password1, method='scrypt')
        elif password1 and password1 != password2:
            flash('Passwords don\'t match.', category='error')

        if contact_number:
            nanny.contact_number = contact_number

        if address:
            nanny.address = address

        if hourly_rate:
            nanny.hourly_rate = hourly_rate

        if years_of_experience:
            nanny.years_of_experience = years_of_experience

        if city:
            nanny.city = city

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.update_nanny_profile'))

    return render_template('nanny_profile.html', nanny=nanny)


@views.route('/family/profile', methods=['GET', 'POST'])
@login_required
def update_family_profile():
    family = current_user

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        preferred_payment_method = request.form.get('preferred_payment_method')

        if email:
            existing_family = Family.query.filter_by(email=email).first()
            if existing_family and existing_family != family:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            else:
                family.email = email

        if first_name:
            if len(first_name) < 2:
                flash('First Name must be greater than 1 character.',
                      category='error')
            else:
                family.first_name = first_name

        if last_name:
            if len(last_name) < 2:
                flash('Last Name must be greater than 1 character.',
                      category='error')
            else:
                family.last_name = last_name

        if password1 and password1 == password2:
            if len(password1) < 7:
                flash('Password must be greater than 7 characters.',
                      category='error')
            else:
                family.password = generate_password_hash(
                    password1, method='scrypt')
        elif password1 and password1 != password2:
            flash('Passwords don\'t match.', category='error')

        if contact_number:
            family.contact_number = contact_number

        if address:
            family.address = address

        if preferred_payment_method:
            family.preferred_payment_method = preferred_payment_method

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('views.update_family_profile'))

    return render_template('family_profile.html', family=family)


@views.route('/family/booking', methods=['GET', 'POST'])
@login_required
def create_family_booking():
    if not current_user.is_family:
        flash('Access denied. Only family users can create bookings.',
              category='error')
        return redirect(url_for('views.home'))

    family = current_user

    # Fetch the bookings for the current family
    bookings = Booking.query.filter_by(family_id=family.id).all()

    if request.method == 'POST':
        nanny_email = request.form.get('nanny_email')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        job_description = request.form.get('job_description')
        status = 'pending'

        # Find the nanny based on the provided email
        nanny = Nanny.query.filter_by(email=nanny_email).first()

        if not nanny:
            flash('Nanny not found.', category='error')
        else:
            # Convert start_date and end_date strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
            # Create a new booking
            booking = Booking(
                family_id=family.id,
                nanny_id=nanny.id,
                start_date=start_date,
                end_date=end_date,
                job_description=job_description,
                status=status
            )
            db.session.add(booking)
            db.session.commit()

            flash('Booking created successfully!', category='success')
            return redirect(url_for('views.create_family_booking'))

    return render_template('family_booking.html', bookings=bookings)


@views.route('/nanny/booking', methods=['GET', 'POST'])
@login_required
def handle_booking():
    if not current_user.is_nanny:
        flash('Access denied. Only nanny users can handle bookings.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        status = request.form.get('status')

        # Find the booking based on the provided booking_id
        booking = Booking.query.get(booking_id)

        if not booking:
            flash('Booking not found.', category='error')
        elif booking.nanny_id != current_user.id:
            flash('You are not authorized to handle this booking.', category='error')
        else:
            booking.status = status
            db.session.commit()

            flash('Booking handled successfully!', category='success')

            # Redirect to the same page to refresh the bookings
            return redirect(url_for('views.handle_booking'))

    bookings = Booking.query.filter_by(nanny_id=current_user.id).all()
    return render_template('nanny_booking.html', bookings=bookings)
