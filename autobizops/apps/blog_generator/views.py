# autobizops/apps/blog_generator/views.py

from flask import render_template, Blueprint, redirect, request, jsonify, json, abort, url_for, flash
from flask_login import login_required, current_user
from autobizops.apps.blog_generator.forms import GenerateBlogPostForm
from autobizops import db
from autobizops.models import Automation, GeneratedBlogPost, BlogPostIteration, User
import requests
import os

blog_generator = Blueprint('blog_post_generator', __name__, url_prefix='/blog_post_generator')
N8N_BLOG_GENERATION_WEBHOOK_URL = os.environ.get('N8N_BLOG_GENERATION_WEBHOOK_URL', '')


@blog_generator.route('/form', methods=['GET', 'POST'])
@login_required
def submit_form():
    form = GenerateBlogPostForm()

    if form.validate_on_submit():
        data = {
            'keyword': form.keyword.data,
            'niche': form.niche.data,
            'target_audience': form.target_audience.data,
            'personal_take': form.personal_take.data
        }

        blog_post = GeneratedBlogPost(
            automation_id=2,
            user_id=current_user.id,
            original_inputs=json.dumps(data),
        )
        db.session.add(blog_post)
        db.session.commit()

        # Send to Webhook N8N_WEBHOOK_URL, params=data to Celery Worker
        from autobizops.celery.tasks import generate_blog_post
        generate_blog_post.delay(blog_post_id=blog_post.id, data=data, webhook_url=N8N_BLOG_GENERATION_WEBHOOK_URL)
        flash("Your Blog Post is being generated. Check back shortly.")

        return redirect(url_for('users.account'))

    return render_template('blog_generator/form.html', form=form)


@blog_generator.route('/<int:blog_post_id>')
@login_required
def blog_post(blog_post_id):

    post = GeneratedBlogPost.query.get_or_404(blog_post_id)
    post_iterations = BlogPostIteration.query.filter_by(blog_post_id=post.id).order_by(BlogPostIteration.creation_date.desc())

    if post.user != current_user:
        abort(403)

    iterations = []
    for iteration in post_iterations:
        i = json.loads(iteration.content_html)
        iterations.append(i['html'])

    return render_template('blog_generator/blog_post.html', post=post, iterations=iterations)




