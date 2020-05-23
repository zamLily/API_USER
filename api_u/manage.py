import os

from flask_migrate import MigrateCommand
from flask_script import Manager

from App import create_app
from App.models.UserModel import Labs, Mentors, Students
from App.ext import db

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = create_app(os.getenv("FLASK_PROJECT") or "default")


#app.config['SECRET_KEY'] = 'secret key here'


manager = Manager(app=app)

manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, Labs=Labs, Mentors=Mentors, Students=Students)

if __name__ == '__main__':
    manager.run(host='0.0.0.0', port=5000)
