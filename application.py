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



#setup
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']="abhinav"

# Check for environment variable


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database

engine = create_engine('postgres://ghavkjvddfqrlb:44d807999d59280b8ab0440d66946f69b2c6601b94d1879574f7ace5e4104899@'
                        'ec2-18-235-97-230.compute-1.amazonaws.com:5432/d9jrtqc0v005hs')
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
        return redirect(url_for('search'))
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(url_for('search'))
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
        return redirect(url_for('search'))
    form=LoginForm()
    if form.validate_on_submit():
        username=request.form.get("username")
        user=db.execute("SELECT * FROM users WHERE username=:username", {"username":username}).fetchone()
        if user:
            password=request.form.get("password")
            if(password==user.password):
                session["username"] = user.username
                session["user_id"] = user.id
                session["email"]=user.email
                return redirect(url_for('search'))
            else:
                return('<h1>Invalidsername/Password</h1>')
        else:
             return('<h1>InvalidUsername/Password</h1>')
                 
        #return('<h1>'+form.username.data+ '</h1>')

    return render_template("login.html", form=form)

@app.route("/search",methods=['GET','POST'])
def search():
    if "username" in session:
        username=session["username"]
        #thisbook=db.execute("SELECT author FROM books WHERE year=1991").fetchone()
        return render_template("search.html",username=username)
    else:
        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        session.pop("user_id")
        session.pop("email")
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route("/booklist",methods=['GET','POST'])
def booklist():
    if "username" in session:
        searchtype=request.form.get("searchtype")
        searchinput=request.form.get("searchinput")
        if searchtype=="year":
            books=db.execute("SELECT * FROM books WHERE year = :searchinput",{"searchinput":searchinput}).fetchall()
        else:    
            books=db.execute("SELECT * FROM books WHERE UPPER(" + searchtype + ") LIKE :searchinput ORDER BY title",{"searchinput":"%" +searchinput.upper() +"%"}).fetchall()
        if books:
            return render_template("booklist.html",books=books)
        return('<h1>Sorry! No matches found</h1>')
    else:
        return redirect(url_for('login'))

@app.route("/bookinfo/<int:book_id>",methods=['POST','GET'])
def bookinfo(book_id):
    if "username" in session and request.method=="GET":
        book=db.execute("SELECT * FROM books WHERE id=:book_id",{"book_id":book_id}).fetchone()
        reviews=db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id JOIN books ON reviews.book_id=books.id WHERE book_id=:book_id", {"book_id":book_id}).fetchall()
        return render_template("bookinfo.html",book=book,reviews=reviews)
    if request.method=="POST":
        user_id=session["user_id"]
        user_review=request.form.get("review")
        user_rating=request.form.get("rating")
        review=db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id JOIN books ON reviews.book_id=books.id WHERE book_id=:book_id AND user_id=:user_id",{"book_id":book_id,"user_id":user_id}).fetchone()
        if review:
            db.execute("UPDATE reviews SET review=:user_review , rating=:user_rating WHERE book_id=:book_id AND user_id=:user_id",
            {"user_review":user_review,"user_rating":user_rating,"user_id":user_id,"book_id":book_id})
            
        else:
            db.execute("INSERT INTO reviews (user_id,book_id,rating,review) VALUES (:user_id,:book_id,:rating,:review)",
            {"user_id":user_id,"book_id":book_id,"rating":user_rating,"review":user_review})
        db.commit()   
        book=db.execute("SELECT * FROM books WHERE id=:book_id",{"book_id":book_id}).fetchone()
        reviews=db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id JOIN books ON reviews.book_id=books.id WHERE book_id=:book_id",{"book_id":book_id}).fetchall()
        
        return render_template("bookinfo.html",book=book,reviews=reviews)
        
    
    else:
        return redirect(url_for('login'))




