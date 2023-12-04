from flask import Flask, render_template, url_for

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)