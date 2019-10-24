from zines import db
from datetime import datetime


class Post(db.Model):
    title = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.UnicodeText)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, unique=True, primary_key=True)

    def __repr__(self):
        return f'<Post; title: {self.title}, id: {self.post_id}>'

