from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

#zainstancjonowanie appki flaskowej
app = Flask(__name__)

#later make it env variable
app.config['SECRET_KEY'] = 'a8a1b7728c69b879f4c218afb8d49e36'

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


@app.route("/register")
def registration():
    form = RegistrationForm()
    return render_template('register.html', title='Registration', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login Page', form=form)


if __name__ == "__main__":
    app.run(debug=True)