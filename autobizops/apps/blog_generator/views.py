# autobizops/apps/blog_generator/views.py

from flask import render_template, Blueprint, redirect

blog_generator = Blueprint('blog_generator', __name__, url_prefix='/blog_generator')


@blog_generator.route('/form')
def form():
    return render_template('blog_generator/form.html')