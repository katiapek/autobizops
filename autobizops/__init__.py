from flask import Flask

app = Flask(__name__)

from autobizops.core.views import core
from autobizops.apps.blog_generator.views import blog_generator
from autobizops.apps.custom_automation.views import custom_automation
app.register_blueprint(core)
app.register_blueprint(blog_generator)
app.register_blueprint(custom_automation)
