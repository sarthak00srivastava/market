from market import app
from market.models import User, Item, db
from market.forms import RegisterForm, LoginForm, PurchaseForm, SellForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/market', methods = ['GET', 'POST'])
@login_required
def market():
    purchase = PurchaseForm()
    sell = SellForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        item = Item.query.filter_by(name=purchased_item).first()
        if item:
            if item.price <= current_user.budget:
                item.owner = current_user.id
                current_user.budget -= item.price
                db.session.commit()
                flash(f'Congratulations! You have successfully purchased {item.name} for ₹{item.price}', 'success')
            else:
                flash('Unfortunately! You are out of budget. Try selling Owned Items.', 'info')
            return redirect(url_for('market'))
        sold_item = request.form.get('sold_item')
        item = Item.query.filter_by(name=sold_item).first()
        if item:
            if item in current_user.items:
                item.owner = None
                current_user.budget += item.price
                db.session.commit()
                flash(f'Congratulations! You have successfully sold {item.name} for ₹{item.price}', 'success')
            else:
                flash('Sorry! There was an unexpected error.', 'info')
            return redirect(url_for('market'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        user_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items = items, user_items = user_items, purchase = purchase, sell = sell)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password1.data
            )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Success! You are registered and logged in as {form.username.data}', 'success')
        return redirect(url_for('market'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], 'warning')
    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user:
            if attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(User.query.filter_by(username=form.username.data).first())
                flash(f'Success! You are logged in as {form.username.data}', 'success')
                return redirect(url_for('market'))
            else:
                flash('Username and Password do not match! Please try again.', 'danger')
        else:
            flash('User do not exist. Please create Account.', 'danger')
            return redirect(url_for('register'))
    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0], 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return render_template('home.html')