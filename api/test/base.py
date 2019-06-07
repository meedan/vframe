from flask_testing import TestCase
from manage import app
from app.models.sql_factory import engine, Base
from app.server.create import db

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        return app

    def setUp(self):
        Base.metadata.create_all(engine)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        Base.metadata.drop_all(engine)
