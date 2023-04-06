import os
import click
from flask_migrate import Migrate
from app import create_app, db
from app.models import User, Role, Permission, Userlog, Userwordrel, Word, Diff, Difftype,Survey,Surveywordrel

# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = create_app('development')

# migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Userlog=Userlog, Userwordrel=Userwordrel, Word=Word,
                Diff=Diff, Difftype=Difftype, Survey=Survey, Surveywordrel=Surveywordrel)

if __name__ == '__main__':
    app.run()
