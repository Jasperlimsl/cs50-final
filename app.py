from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '8615288dd655ead7ac3e53c23e1679810038'

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
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash(f'Welcome {form.username.data}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form=form)

if __name__ == '__main__':
    app.run(debug=True)