from flask import render_template
from . import app
from . import models

@app.route('/post/')
@app.route('/post/<post_id>')
def index(post_id=None):
    post = models.Post.query.filter_by(post_id=post_id).first()
    # post = {'title': 'The Great Corn Heist',
    #        'content': content}
    return render_template('post.html', post=post)
