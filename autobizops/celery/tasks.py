from autobizops.models import GeneratedBlogPost, BlogPostIteration
from autobizops import celery_app, db, app
from flask_login import current_user
from flask import json
import requests


@celery_app.task(bind=True, soft_time_limit=960, time_limit=1020 )
def generate_blog_post(self, blog_post_id, data, webhook_url):
    try:
        res = requests.get(webhook_url, params=data, timeout=900)
        res.raise_for_status()

        # When everything is fine, create a blog post
        blog_post = GeneratedBlogPost.query.get(blog_post_id)
        if not blog_post:
            return {'status': 'Error', 'message': 'Blog post not found'}

        # save content as String
        blog_post_iteration = BlogPostIteration(content_html=json.dumps(res.json()[0]))
        # add relationship
        blog_post.iterations_rel.append(blog_post_iteration)
        blog_post.status = 'Completed'

        db.session.add(blog_post_iteration)
        db.session.commit()

        return {'status': 'completed', 'blog_post_id': blog_post_id}
    except Exception as e:
        blog_post = GeneratedBlogPost.query.get(blog_post_id)
        if blog_post:
            blog_post.status = 'Failed'
            db.session.commit()
        return {'status': 'error', 'message': str(e)}
