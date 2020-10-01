# one time run script to update markdown field
from zines import db
from zines.models import Post
import html2markdown as h2m
from bs4 import BeautifulSoup


innerHTML = lambda post : "".join([str(x) for x in BeautifulSoup(post.content).div.contents])
posts = Post.query.all()

for p in posts:
    md = "# " + str(p.title) + "\n"
    md += innerHTML(p)
    p.markdown = h2m.convert(md)
    db.session.commit()
