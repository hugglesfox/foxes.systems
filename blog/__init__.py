from flask import Flask, render_template
from .post import Posts
from .renderer import md

CONTENT_PATH = 'content'
POST_PATH = CONTENT_PATH + '/posts'

app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        posts=Posts(POST_PATH).sorted(),
        enumerate=enumerate)


@app.route('/archive/')
def archive():
    return render_template(
        'archive.html',
        posts=Posts(POST_PATH).sorted(),
        enumerate=enumerate)


@app.route('/post/<name>/')
def post(name):
    return render_template('content.html', content=Posts(POST_PATH).get(name).render())


@app.route('/about/')
def about():
    with open(CONTENT_PATH + '/about.md') as f:
        return render_template('content.html', content=md.render(f.read()))
