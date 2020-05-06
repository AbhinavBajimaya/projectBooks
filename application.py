import os

from flask import Flask, session,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,email_validator,Length,Email



app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']="abhinav"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class LoginForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=18)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=18)])
    remember=BooleanField('Remember me')

class RegisterForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=18)])
    email=StringField('email',validators=[InputRequired(), Email(), Length(max=50)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=18)])




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        return('<h1>'+form.username.data+ '</h1>')

    return render_template("register.html", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        return('<h1>'+form.username.data+ '</h1>')

    return render_template("login.html", form=form)




