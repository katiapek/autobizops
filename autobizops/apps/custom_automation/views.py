from flask import Blueprint, render_template
from flask_login import login_required

custom_automation = Blueprint('custom_automation', __name__, url_prefix='/custom_automation')


@custom_automation.route('/form')
@login_required
def submit_form():
    return render_template('custom_automation/form.html')