from flask import Flask, render_template, url_for
#zainstancjonowanie appki flaskowej
app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)