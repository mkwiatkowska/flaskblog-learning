from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect

posts = [
    {
        'author': 'Maria Kwiatkowska',
        'title': 'flaskblog',
        'content': 'testing post',
        'date_posted': '23-03-2019'
    },
    {
        'author': 'Jan Nowak',
        'title': 'Jan Blog',
        'content': 'Post Janka',
        'date_posted': '03-02-2019'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Ur account has been created! U can now log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Registration', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@py.com' and form.password.data == 'admin':
            flash('u have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('couldnt log u in, sorry', 'danger')
    return render_template('login.html', title='Login Page', form=form)
