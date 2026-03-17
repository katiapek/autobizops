from autobizops.models import Automation
from autobizops import app, db

with app.app_context():
    automation1 = Automation.query.filter_by(name='Blog Post Generator').first_or_404()
    automation1.url_prefix = '/blog_post_generator'

    db.session.add(automation1)
    db.session.commit()
