from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import ContactForm #, LoginForm, EditForm
# from .models import User

@app.before_request
def before_request():
    g.user = current_user

@app.route('/appointments')
def appointments():
    return render_template("appointments.html",
                           title='Appointments',
                           company_name=company_name,
                           year=year)

@app.route('/register')
def register():
    return render_template("register.html",
                           title='Register',
                           company_name=company_name,
                           year=year)

@app.route('/login')
def login():
    return render_template("login.html",
                           title='Login',
                           company_name=company_name,
                           year=year)

@app.route('/admin_interface')
def admin_interface():
    return render_template("admin_interface.html",
                           title='Admin_Interface',
                           company_name=company_name,
                           year=year)  