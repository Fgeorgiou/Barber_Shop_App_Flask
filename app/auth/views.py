from flask import flash, redirect, request, render_template, url_for
from flask_login import login_required, login_user, logout_user
from datetime import datetime
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

#global variables
company_name = {'name' : 'LaKosta'} # Test
year = datetime.now().year

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error), 'error')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    #Add a user to the database through the registration form

    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        birth_date=form.birth_date.data,
                        email=form.email.data,
                        telephone=form.telephone.data,
                        password=form.password.data)

            # add user to the database
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered! You may now login!', 'info')

            # redirect to the login page
            return redirect(url_for('auth.login'))
        else :
            flash_errors(form)

        # load registration template
        return render_template('auth/register.html', form=form,
                                                    title='Register',
                                                    company_name=company_name,
                                                    year=year)

    elif request.method == 'GET':
        # load registration template
        return render_template("auth/register.html",
                           title='Register',
                           company_name=company_name,
                           year=year,
                           form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log a user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)

            #if user is admin, redirect to admin interface
            if user.is_admin:
                return redirect(url_for('admin.admin_interface')) 
            else:
                # else redirect to index page
                return redirect(url_for('home.index'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form,
                                            title='Login',
                                            company_name=company_name,
                                            year=year)

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.', 'info')

    # redirect to the login page
    return redirect(url_for('home.index'))