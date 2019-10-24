from flask import render_template, request
from . import app, db
from . import models
from .forms import CreatePost
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup


@app.route('/')
@app.route('/index')
def index():
    posts = models.Post.query.all()
    return render_template("index.html", posts=posts)
@app.route('/post/')
@app.route('/post/<post_id>')
def post(post_id=None):
    post = models.Post.query.filter_by(post_id=post_id).first()
    soup = BeautifulSoup(post.content, 'html.parser')
    sections = soup.find_all(['h1', 'h2', 'h3'])
    sections = [section.get_text() for section in sections]
    print(sections)
    return render_template('post.html', post=post, sections=sections)

@app.route('/write', methods=["GET", "POST"])
def write():
    form = CreatePost()
    if request.method == "POST":
        cleaner = Cleaner(allow_tags=['p', 'h1', 'h2', 'h3'],
                          remove_unknown_tags=False)
        post = cleaner.clean_html(request.form.get('delta'))
        soup = BeautifulSoup(post, 'html.parser')
        title = soup.find_all('h1')[0].string # todo: check if exists first
        for h1 in soup("h1"): # remove all h1 tags
            h1.decompose()

        post=soup.prettify()
        submission = models.Post(title=title, author="meb", content=post)
        db.session.add(submission)
        db.session.commit()
        print(f"Title: {title}" )
    return render_template('write.html', form=form)
