import os
import time
from flask import render_template, request, redirect, flash, url_for, send_from_directory, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from . import app, db
from . import models
from .forms import CreatePost, LoginForm
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
from types import SimpleNamespace
from markdown import markdown


@app.route('/')
@app.route('/index')
def index():
    blog_title = app.config['TITLE']
    blog_description = app.config['DESCRIPTION']
    posts = models.Post.query.filter(models.Post.hidden != True).order_by(models.Post.date.desc()).all() 
    previews = {post.post_id:BeautifulSoup(post.content).p.text for post in posts}
    #{post.post_id:BeautifulSoup(post.content).get_text(" ", strip=True)[:500] + "..." for post in posts}
    return render_template("index.html", posts=posts, blog_title=blog_title, blog_description=blog_description, previews=previews)

@app.route('/post/<post_id>')
def post(post_id=None):
    blog_title = app.config['TITLE']
    blog_description = app.config['DESCRIPTION']
    post = models.Post.query.filter_by(post_id=post_id).first()
    soup = BeautifulSoup(post.content, 'html.parser')
    # assign section ids
    sections = soup.find_all(['h1', 'h2', 'h3'])
    for i, tag in enumerate([tag for tag in soup.find_all(['h2', 'h3'])]):
        tag['id'] = i+1 # hacky shit
        soup.find(['h2', 'h3'], text=tag.text).replace_with(tag)
    post_view = SimpleNamespace(**{"content":soup.div, "author":post.author, "title":post.title, "images":post.images})
    sections = [section.get_text() for section in sections]
    return render_template('post.html', blog_title=blog_title, blog_description=blog_description, post=post_view, sections=sections)

@app.route('/write/<post_id>', methods=["GET", "POST"])
@app.route('/write', methods=["GET", "POST"])
@login_required
def write(post_id=None):
    if request.method == "POST":
        # get markdown, convert it to html, then save both
        data = request.json
        # print(data['content'])
        md = data['content']
        html = markdown(md)
        # get info and save to database
        cleaner = Cleaner(allow_tags=['p', 'h1', 'h2', 'h3', 'a', 'blockquote', 'ul', 'ol', 'li', 'pre', 'code'],
                        remove_unknown_tags=False)
        post = cleaner.clean_html(html)
        soup = BeautifulSoup(post, 'html.parser')
        title = soup.find_all('h1')[0].string # todo: check if exists first
        for h1 in soup("h1"): # remove all h1 tags
            h1.decompose()
        post = str(soup)
        submission = models.Post(title=title, author=current_user.username, content=post, markdown=md)
        db.session.add(submission)
        db.session.commit()
        return jsonify(dict(message="Received"))
    elif request.method == "GET" and post_id != None:
        # grab the md to edit
        md = models.Post.query.filter_by(post_id=post_id).first()
    return render_template('write.html')

@app.route('/md/<post_id>')
def fetch_post(post_id):
    md = models.Post.query.filter_by(post_id=post_id).first()
    return jsonify(md=md.markdown)

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


# Functions below are functional with config set up but we need to make them upload filename (timestamp)
# to database and associate with blog post id. Then we will need to make templates display the image if
# one exists or a default image otherwise.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/image', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            basedir = os.path.abspath(os.path.dirname(__file__))
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload/post', methods=['GET', 'POST'])
@login_required
def upload_post():
    # todo: make sure to save markdown
    if request.method == 'POST':
        # ensure the post request has file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # get the markdown from the file
            md = markdown(file.read().decode('utf-8')) # convert md from bytes to utf-8 string then convert to markdown
            file.close()
            # get info and save to database
            cleaner = Cleaner(allow_tags=['p', 'h1', 'h2', 'h3', 'a', 'blockquote', 'ul', 'ol', 'li', 'pre', 'code'],
                          remove_unknown_tags=False)
            post = cleaner.clean_html(md)
            soup = BeautifulSoup(post, 'html.parser')
            title = soup.find_all('h1')[0].string # todo: check if exists first
            for h1 in soup("h1"): # remove all h1 tags
                h1.decompose()
            post = str(soup)
            submission = models.Post(title=title, author=current_user.username, content=post)
            db.session.add(submission)
            db.session.commit()
            return redirect(url_for('index'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/edit/image/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_image(post_id):
    if request.method == 'POST':
        if 'file' not in request.files:
            # if post request has no file part
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # save image, and make database record to link to post 
            basedir = os.path.abspath(os.path.dirname(__file__))
            file_type = os.path.splitext(file.filename)[1]
            filename = str(time.time())[:16].replace('.', '') # secure_filename(file.filename) # TODO: make this a timestamp
            file_record = models.Image(id=int(filename), url=filename+file_type, post_id=post_id)
            db.session.add(file_record)
            db.session.commit()
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename+file_type)) 
            flash("File uploaded!")
            return redirect(url_for('post', post_id=post_id))
    return '''
    <!doctype html>
    <h1>Edit Image</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
    </form>
    '''