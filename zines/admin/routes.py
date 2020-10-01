from flask import jsonify, render_template, request
from zines import app, db
from zines.models import Post, Image
from flask_login import login_required
from . import admin


@admin.route('/posts')
def get_posts():
    posts = Post.query.order_by(Post.date.desc()).all()
    posts = [dict((col, getattr(post, col)) for col in Post.__table__.columns.keys() if col != 'content') for post in posts]
    return jsonify(posts)

@app.route('/images')
@login_required # don't make it easy to snoop
def get_images():
    images = Image.query.all()
    images = [dict((col, getattr(image, col)) for col in Image.__table__.columns.keys()) for image in images]
    return jsonify(images)

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

@app.route('/delete/<post_id>', methods=["DELETE"])
@login_required
def delete(post_id):
    # verify user is logged in and associated with post
    Post.query.filter_by(post_id=post_id).delete()
    db.session.commit()
    return jsonify(
        dict(message=f"Post {post_id} deleted")
    )

@app.route('/images/<image_id>/delete', methods=['DELETE'])
@login_required
def delete_image(image_id):
    Image.query.filter_by(id=image_id).delete()
    db.session.commit()
    return jsonify(
        dict(message=f"Image {image_id} deleted")
    )
