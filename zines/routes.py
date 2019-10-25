from flask import render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from . import app, db
from . import models
from .forms import CreatePost, LoginForm
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup


@app.route('/')
@app.route('/index')
def index():
    blog_title = app.config['TITLE']
    posts = models.Post.query.all()
    return render_template("index.html", posts=posts, blog_title=blog_title)
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
@login_required
def write():
    # todo: make first h1 the title, make all other h1s into h2s
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

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # POST
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password') # base.html has no way to intercept these so flashes don't show on login page
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('index'))
