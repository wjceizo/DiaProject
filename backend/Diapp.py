#!/usr/bin/python3

import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission, Userlog, Userwordrel, Word, Diff, Difftype,Survey,Surveywordrel
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.abspath(os.getcwd()), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_ENV') or 'default')

# migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Userlog=Userlog, Userwordrel=Userwordrel, Word=Word,
                Diff=Diff, Difftype=Difftype, Survey=Survey, Surveywordrel=Surveywordrel)

if __name__ == '__main__':
    import bjoern

    bjoern.run(app, "127.0.0.1", 5000)
