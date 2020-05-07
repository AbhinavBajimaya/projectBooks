#do the imports here
import os
from flask import Flask, session,render_template,request,flash,redirect,url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,email_validator,Length,Email
import requests
#from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user


#setup
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


#Login form
class LoginForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=18)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=18)])
    remember=BooleanField('Remember me')

#Registration form
class RegisterForm(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=18)])
    email=StringField('email',validators=[InputRequired(), Email(), Length(max=50)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=18)])


#Routes
@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(url_for('dashboard'))
    form=RegisterForm()
    if form.validate_on_submit():
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        db.execute("INSERT INTO users (username,email,password) VALUES (:username,:email,:password)",
        {"username":username,"email":email,"password":password} )
        db.commit()
        #flash('Registered succesfully')   
       # return render_template("index.html",message="Registration Successful")
    
    return render_template("register.html", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect(url_for('dashboard'))
    form=LoginForm()
    if form.validate_on_submit():
        username=request.form.get("username")
        user=db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchone()
        if user:
            password=request.form.get("password")
            if(password==user.password):
                session["username"] = user.username
                session["id"] = user.id
                session["email"]=user.email
                return redirect(url_for('dashboard'))
            else:
                return('<h1>Invalidsername/Password</h1>')
        else:
             return('<h1>InvalidUsername/Password</h1>')
                 
        #return('<h1>'+form.username.data+ '</h1>')

    return render_template("login.html", form=form)

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if "username" in session:
        username=session["username"]
        return render_template("dashboard.html",username=username)
    else:
        return redirect(url_for('login'))
    




