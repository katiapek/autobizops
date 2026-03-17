# autobizops/users/views.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from autobizops.users.forms import RegistrationForm, LoginForm
from autobizops.models import User, GeneratedBlogPost
from autobizops import db
import json
from datetime import datetime

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash("User registered successfully. Please log-in.", "success")
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None:
            flash('Invalid e-mail or password.','danger')
            return redirect(url_for('users.login'))

        if user.check_password(form.password.data):
            login_user(user)

            next_page = request.args.get('next')

            if not next_page or not next_page.startswith('/'):
                next_page = url_for('core.index')
            return redirect(next_page)
        else:
            flash('Invalid e-mail or password.', 'danger')
            return redirect(url_for('users.login'))

    return render_template('login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/account')
@login_required
def account():
    # Show user's requests
    user = User.query.filter_by(username=current_user.username).first_or_404()
    user_blog_posts = (GeneratedBlogPost
                       .query.filter_by(user=user)
                       .order_by(GeneratedBlogPost.creation_date.desc())
                       .all())
    post_template = []
    for post in user_blog_posts:
        post_template.append({
            'id': post.id,
            'automation': post.automation.name,
            'automation_url': post.automation.url_prefix,
            'creation_date': post.creation_date.strftime('%Y-%m-%d'),
            'keyword': json.loads(post.original_inputs)['keyword'],
            'status': post.status
        })

    return render_template('account.html', user_blog_posts=post_template)
