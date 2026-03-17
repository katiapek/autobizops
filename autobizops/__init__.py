from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from celery import Celery, Task
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

########################
# DataBase Setup #######
########################
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///fallback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#################
# Login Configs #
#################
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

###########################
# BluePrints Registration #
###########################
from autobizops.core.views import core
from autobizops.apps.blog_generator.views import blog_generator
from autobizops.apps.custom_automation.views import custom_automation
from autobizops.users.views import users
app.register_blueprint(core)
app.register_blueprint(blog_generator)
app.register_blueprint(custom_automation)
app.register_blueprint(users)


###############
# SECRET KEY ##
###############
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-before-deploy')


##############
# CELERY #####a
##############

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(app.name, task_cls=FlaskTask, include=['autobizops.celery.tasks'])
    celery.config_from_object(app.config["CELERY"])
    celery.set_default()
    app.extensions["celery"] = celery
    return celery


app.config["CELERY"] = {
    'broker_url': os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    'result_backend': os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    'task_ignore_result': True
}

celery_app = celery_init_app(app)
