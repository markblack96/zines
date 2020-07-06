from flask import jsonify, render_template
from zines import app, db
from zines.models import Post
from flask_login import login_required
from . import admin

@admin.route('/posts')
def get_posts():
    posts = Post.query.all()
    posts = [dict((col, getattr(post, col)) for col in Post.__table__.columns.keys() if col != 'content') for post in posts]
    return jsonify(posts)

@admin.route('/admin')
@login_required
def admin_panel():
    blog_title = app.config['TITLE']
    blog_description = app.config['DESCRIPTION']
    return render_template('admin.html', blog_title=blog_title, blog_description=blog_description)

@admin.route('/hide/<post_id>', methods=['PATCH'])
@login_required
def hide_post(post_id):
    p = Post.query.filter_by(post_id=post_id).first()
    p.hidden = not p.hidden
    db.session.commit()

    return jsonify(
        dict((col, getattr(p, col)) for col in Post.__table__.columns.keys() if col != 'content')
    )