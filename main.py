from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import count, user
from sqlalchemy.sql import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:password@localhost/adspend-app'
app.config['SECRET_KEY'] = "test"

db=SQLAlchemy(app)

#instantiating, intializing login manager
login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#instantiate user class

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30), unique=True)
    password = db.Column(db.String, unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


@login_manager.user_loader
def load(user_id):
    return User.query.get(int(user_id))


##### Routes #####
@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        username=request.form.get("username")
        password = request.form.get("password")

        user=User.query.filter_by(username=username).first()
        print("here is the username" + username)
        print(User)
        print(user)
        print(user.password)
        print(password)

        
        if not user or not check_password_hash(user.password, password):
            flash("This user does not exist!")
            return redirect(url_for('login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('home'))

    return render_template('login.html')
  
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

  
@app.route('/signup')
def signup():
    return render_template("signup.html")



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)



