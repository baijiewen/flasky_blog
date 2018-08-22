import os
COV = None
if os.environ.get('FLASK_COVERAGE'): #or app.config['FLASK_COVERAGE']:
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

import sys
import click
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage=False):
    if coverage and not os.environ.get('FLASK_COVERAGE'):#app.config['FLASK_COVERAGE']:

        import subprocess
        os.chdir('F:\Users\hp\PycharmsProjects\untitled3\Lib\site-packages\pytesser')
        os.environ['FLASKY_COVERAGE'] = '1'

        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()
