from flask import Blueprint, render_template

custom_automation = Blueprint('custom_automation', __name__, url_prefix='/custom_automation')


@custom_automation.route('/form')
def form():
    return render_template('custom_automation/form.html')