from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    instagram = db.Column(db.String(50), unique=True)
    twitter = db.Column(db.String(50), unique=True)
    facebook = db.Column(db.String(50), unique=True)
    snapchat = db.Column(db.String(50), unique=True)
    linkedin = db.Column(db.String(50), unique=True)
    tiktok = db.Column(db.String(50), unique=True)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            return redirect(url_for('home', username=username))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/home/<username>')
def home(username):
    user = User.query.filter_by(username=username).first()
    accounts = {
        'instagram': user.instagram,
        'twitter': user.twitter,
        'facebook': user.facebook,
        'snapchat': user.snapchat,
        'linkedin': user.linkedin,
        'tiktok': user.tiktok,
    }
    return render_template('home.html', accounts=accounts, user=user)

@app.route('/add_account/<username>', methods=['GET', 'POST'])
def add_account(username):
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        username = request.form['username']
        platform = request.form['platform']
        account = request.form['account']
        user = User.query.filter_by(username=username).first()
        setattr(user, platform, account)
        db.session.commit()
        return redirect(url_for('home', username=username))
    else:
        return render_template('add_account.html', user=user)

@app.route('/search/<username>', methods=['POST'])
def search(username):
    search_term = request.form['search']
    user = User.query.filter_by(username=search_term).first()
    if user:
        accounts = {
            'instagram': user.instagram,
            'twitter': user.twitter,
            'facebook': user.facebook,
            'snapchat': user.snapchat,
            'linkedin': user.linkedin,
            'tiktok': user.tiktok,
        }
        return render_template('user.html', user=user, accounts=accounts, username=username)
    return redirect(url_for('home', username=username))

@app.route('/user/<username>', methods=['GET'])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        accounts = {
        'instagram': user.instagram,
        'twitter': user.twitter,
        'facebook': user.facebook,
        'snapchat': user.snapchat,
        'linkedin': user.linkedin,
        'tiktok': user.tiktok,
        }
        return render_template('user.html', user=user, accounts=accounts, username=username)
    return redirect(url_for('home', username=username))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)






