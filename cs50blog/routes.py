from flask import render_template, url_for, flash, redirect, request
from cs50blog.forms import RegisterForm, LoginForm
from cs50blog.models import User, Post
from cs50blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts = [{"id":"Andrew", "title":"First Post", "content":"this is the first post of the blog", "date_posted":"YY MM DD"},
{"id":"Bobby", "title":"Second Post", "content":"this is the second post of the blog", "date_posted":"YY MM DD"}
]

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # login_user will login the user and second argument is optional on whether to remember the user
            login_user(user, remember=form.remember.data)
            requested_page = request.args.get('next')
            if requested_page:
                return redirect(requested_page) 
            else:
                return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


