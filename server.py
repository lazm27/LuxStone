import webbrowser
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
app = Flask(__name__)
db_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'project.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["SECRET_KEY"] = "abc"
db=SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fullname=db.Column(db.String(200),nullable=False)
    emailid=db.Column(db.String(200),unique=True,nullable=False)
    username=db.Column(db.String(200),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)
class Item(db.Model):
    itemid=db.Column(db.Integer,primary_key=True)
    userid=db.Column(db.Integer, db.ForeignKey(User.id))
    name=db.Column(db.String(200))
    img=db.Column(db.String(100),unique=True)
    
       
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"An error occurred while creating the database: {str(e)}")


@login_manager.user_loader
def loader_user(user_id):
	return User.query.get(user_id)

@app.route('/')
def hello():
    return render_template('home.html')
@app.route('/home')
def home():
    return render_template("second_home.html")
@app.route('/explore')
def explore():
    return render_template("explore.html")
@app.route('/add_like',methods=["POST","GET"])
def add_like():
    if request.method=="POST":
        detail1=request.form.get("desc")
        detail2=request.form.get("img_data")
        item=Item(userid=current_user.id,name=detail1,img=detail2)
        existing_item=Item.query.filter_by(userid=current_user.id, name=detail1, img=detail2).first()
        if not existing_item:
            db.session.add(item)
            db.session.commit()
            flash("Added to Liked")
        else:
            flash("Already in Liked")
            
        return redirect("/explore")
    
    return redirect("/explore")
@app.route('/like')
def like():
    items=Item.query.filter_by(userid=current_user.id).all()
    return render_template("like.html",items=items)
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        info1=request.form.get("fullname")
        info2=request.form.get("email")
        info3=request.form.get("username")
        info4=request.form.get("password")
        person=User(fullname=info1,emailid=info2,username=info3,password=info4)
        db.session.add(person)
        db.session.commit()
        return render_template("home.html")
    return render_template("signup.html")
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        person=User.query.filter_by(emailid=request.form.get("email")).first()
        if person.password== request.form.get("password"):
            login_user(person)
            return render_template("second_home.html")
    return redirect("/")
        

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")
        

if __name__ == '__main__':
    app.run(debug=True,port=5500)