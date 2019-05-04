from models import User, Post


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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    
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