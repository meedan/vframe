import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.server.create import create_app, db
from app.server.api import api as blueprint

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
  port = os.getenv('VFRAME_PORT') or 5000
  app.run(host='0.0.0.0', port=port, threaded=True)

@manager.command
def test():
  """Runs the unit tests."""
  tests = unittest.TestLoader().discover('./test', pattern='test*.py')
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
  manager.run()
