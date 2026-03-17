# autobizops/models.py
from flask import url_for
from flask_login import UserMixin
from autobizops import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

CREDIT_REGISTRATION_GIFT = 25


# User Loader required by Flask
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class BlogPostIteration(db.Model):
    __tablename__ = 'blog_post_iterations'

    id = db.Column(db.Integer, primary_key=True)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('generated_blog_posts.id'), nullable=False)
    content_html = db.Column(db.String, nullable=False)
    content_markdown = db.Column(db.String)
    user_comments = db.Column(db.String)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, content_html):
        self.content_html = content_html


class BlogPostContext(db.Model):
    __tablename__ = 'blog_post_contexts'

    id = db.Column(db.Integer, primary_key=True)
    blog_post_id = db.Column(db.Integer, db.ForeignKey('generated_blog_posts.id'), nullable=False)
    context_txt = db.Column(db.String)
    research_txt = db.Column(db.String)
    ideas_txt = db.Column(db.String)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)


class GeneratedBlogPost(db.Model):

    __tablename__ = 'generated_blog_posts'

    iterations_rel = db.relationship(BlogPostIteration, backref='blog_post', lazy=True, cascade='all, delete-orphan')
    context_rel = db.relationship(BlogPostContext, backref='blog_post', lazy=True, cascade='all, delete-orphan')

    id = db.Column(db.Integer, primary_key=True)
    automation_id = db.Column(db.Integer, db.ForeignKey('automations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    original_inputs = db.Column(db.String, nullable=False)
    content_html = db.Column(db.String)
    content_markdown = db.Column(db.String)
    status = db.Column(db.String, nullable=False, default='Pending')
    no_of_iterations = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, automation_id, user_id, original_inputs):
        self.automation_id = automation_id
        self.user_id = user_id
        self.original_inputs = original_inputs
        self.no_of_iterations = 1


# Model for users table
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    blog_post_rel = db.relationship(GeneratedBlogPost, backref='user', lazy=True)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    credits_balance = db.Column(db.Integer)
    industry = db.Column(db.String(64))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.credits_balance = CREDIT_REGISTRATION_GIFT

    def __repr__(self):
        return f"{self.username}, {self.email}, has {self.credits_balance} credits left"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Create db.Model for accessible automations
class Automation(db.Model):
    __tablename__ = 'automations'

    blog_post_rel = db.relationship(GeneratedBlogPost, backref='automation', lazy=True)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    cost = db.Column(db.Integer)
    url_prefix = db.Column(db.String(64))

    def __init__(self, name, cost, url_prefix):
        self.name = name
        self.cost = cost
        self.url_prefix = url_prefix

    def __repr__(self):
        return f"{self.id} {self.name} {self.cost}"

