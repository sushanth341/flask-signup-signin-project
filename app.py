
from flask import Flask, render_template, request, redirect, url_for, flash
from extension import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import re  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 


db.init_app(app)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('thankyou'))
        flash('Entered Invalid email or password.')
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.')
            return redirect(url_for('signup'))

       
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('signup'))

      
        password_criteria = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$')
        if not password_criteria.match(password):
            flash('Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one number, and one special character.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign up successful!')
        return redirect(url_for('thankyou'))
    
    return render_template('signup.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/secret')
def secret_page():
    return render_template('secretPage.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
