# CS50 Blog
#### Video Demo: https://www.youtube.com/watch?v=UJBK5jUPH7Y
#### Description: My final project for CS50x is a blog created using Flask-Python. 

#### HTML, CSS, Javascript: The Flask Application uses bootstrap CSS and Javascript to style the HTML templates for aesthetics. 

#### Database: I used the SQLAlchemy Object Relational Mapper (ORM) to create the database for my project. The advantage of this is that it provides the flexibility to use different databases without changing the underlying python code in the future if i wish to expand upon the project. In this project, I use sqlite for a simple database to records information of Users and their blogposts.

#### Web-App is structured as a package. During the creation of my project, I came across an error known as Circular-import error. This was because my files were too interconnected after awhile and were importing elements from each other leading to the circular import error. To resolve this, I restructured the project into a package called cs50blog with a __init__.py file inside.

#### Forms - Flask-WTF with FlaskForm base class and wtforms library: The web-app uses the WTForms form-handling library in python to better manage formss using field classes like "StringField", "BooleanField" etc. It also allows me to use useful methods like "validate_on_submit() to check if the information input into the forms are valid. 

#### Session Management and User Authentication - I use flask-login and its methods to manage users logging in and out, and manage user sessions. In addition, I use flask-bcrypt to encrypt passwords

## Functionalities 
#### Registration and Display pic: The CS50 Blog I created allows users to register with a username, email and password. There is a default display pic allocated to the user, but he can change it at the account page once he has created his account.
#### Blog Posts: Each registered user may create blog posts which are displayed on the homepage sorted by the latest to oldest post. Users may click on an author of the post to see all posts by said author or they can click on the title of a post to see the post by itself. If the user clicks on his own post, the option is available to update/delete the post. However, users cannot update or delete other users' posts.
#### Account Page: Once Logged in, the user may change his username, email and profile pic. The web-app resizes the uploaded profile pic into an output_size = (125, 125) to save storage space and allow the app to run efficiently. In this web-app, I only allowed the upload of jpg and png formats for the profile pic. 
#### Forgot Password: At the login page, the user may click the "forgot Password" link to reset his/her password. To do so, they need to input a registered email in to the Email field. The web-app then cross-checks it with the database and if it is a valid email address that was registered, a password reset email is sent to the user. This functionality was enabled using the Message class that is part of the flask-mail extension. To ensure that the reset process is secure, I used the URLSafeTimedSerializer class from itsdangerous.url_safe library, which is designed to generate URL-safe, tamper-resistant tokens that can be included in URLs. The token expiration is set to 1800s in the web-app.
#### Flash Messages: The web application uses flash messages to inform users when a certain action has been completed for example when a post has been created, amended or deleted.
#### Error handling: In the routes.py file, I user @app.errorhandler to handle common errors such as 404, 403 and 500. The user is directed to a page showcasing the error. 
#### Pagination: The paginate method from flask_sqlalchemy is used to split the blog posts into pages and allow users to navigate between pages. For my blog, each page shows a maximum of 5 posts. 

## Files and their Functions
#### The main folder is CS50-FINAL and within it is a 'run.py' file that runs the flask application. The 'cs50blog' folder is a package that contain a __init__.py file to run the application properly. 'routes.py' is a file containing all the routes in the application that links to the various html templates in the templates folder. 'models.py' is a file that defines the User and Post Class for the database. 'forms.py' is the file that contains all the forms used by the application. As previously mentioned, I used Flask-WTF with FlaskForm base class and wtforms library to manage the forms in the application. 
#### The static folder within cs50blog contains the 'main.css' file which contains the css classes on top of bootstrap classes loaded into the html templates. The static folder also contains a folder called 'profile_pics' to hold all the profile pics uploaded by the user.
#### There is also an 'instance' folder that contains the blog.db file, which is the database file of the application.
#### the requirement.txt file contains all the required libraries and modules to run the application properly.