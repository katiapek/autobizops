# autobizops/apps/blog_generator/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class GenerateBlogPostForm(FlaskForm):
    keyword = StringField('Targeted Keyword: ', validators=[DataRequired()])
    niche = StringField('Industry Niche: ', validators=[DataRequired()])
    target_audience = StringField('Target Group: ', validators=[DataRequired()])
    personal_take = TextAreaField('Personal take: ', validators=[DataRequired()])
    submit = SubmitField('Generate Post')


class BlogPostCorrectionForm(FlaskForm):
    comments = TextAreaField('Corrective instructions', validators=[DataRequired()])
    submit = SubmitField()

