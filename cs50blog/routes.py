import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from cs50blog.forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from cs50blog.models import User, Post
from cs50blog import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def index():
    page = request.args.get('page', 1, type=int)
    # Grab all the posts data in the database
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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

@app.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Post is the class created in models.py file. The data collected by the form in the new_post.html is parsed in so that it can be uploaded to the database.
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        # add the post to the database and commit it.
        db.session.add(post)
        db.session.commit()

        # Create Flash Message to notify user that the post had been created, and direct the user back to the homepage.
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('new_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    # Get the post with the post_id, else give a 404 error
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # Get the post with the post_id, else give a 404 error
    post = Post.query.get_or_404(post_id)
    # Only allow the creator of the post to adit it
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your Post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    # fill in the form with the post's original content to make it easier for users to amend
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('new_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    # Get the post with the post_id, else give a 404 error
    post = Post.query.get_or_404(post_id)
    # Only allow the creator of the post to adit it
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted!', 'success')
    return redirect(url_for('index'))

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)

def send_reset_email(user):
    # default set by me is 1800s
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' Your username is {user.username}
To reset your password, please visit this link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated! Please login with your new password', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/404.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/404.html'), 500