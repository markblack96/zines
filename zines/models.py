from zines import db, login
from datetime import datetime
import jwt
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Post(db.Model):
    title = db.Column(db.String)
    author = db.Column(db.String, db.ForeignKey('user.id'))
    content = db.Column(db.UnicodeText)
    markdown = db.Column(db.UnicodeText)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, unique=True, primary_key=True)
    images = db.relationship('Image', backref='post', lazy=True)
    hidden = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<Post; title: {self.title}, id: {self.post_id}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)

    
class Image(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    url = db.Column(db.String(128), unique=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))