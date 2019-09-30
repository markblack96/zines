from zines import db

class Post(db.Model):
    title = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.UnicodeText)
    post_id = db.Column(db.Integer, unique=True, primary_key=True)

    def __repr__(self):
        return '<Post %r>' % self.post_id

