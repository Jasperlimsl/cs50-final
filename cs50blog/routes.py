import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from cs50blog.forms import RegisterForm, LoginForm, UpdateAccountForm
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

def save_picture(form_picture):
    random = secrets.token_hex(8)
    # since we are not using f_name, we replace it with just an underscore
    # f_name, f_ext = os.path.splitext(form_picture.filename)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    # Delete the old profile picture if it exists
    if current_user.image_file != 'default.jpg':
        old_picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)

    
    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


