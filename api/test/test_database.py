import unittest
import json
from flask import current_app as app

from test.base import BaseTestCase
from app.server.create import db
from app.models.sql_factory import add_phash, search_by_phash

class TestDatabase(BaseTestCase):
  def test_bitcount(self):
    self.assertEqual(2, db.session.execute('SELECT bit_count(5)').first()[0])

  def test_jsonb(self):
    self.assertEqual(True, db.session.execute('SELECT \'{"context": {"team_id": 1, "project_id": 2, "project_media_id": 3}}\'::jsonb @> \'{"context": { "project_id": 2 }}\'::jsonb').first()[0])
    self.assertEqual(False, db.session.execute('SELECT \'{"context": {"team_id": 1, "project_id": 2, "project_media_id": 3}}\'::jsonb @> \'{"context": { "project_id": 3 }}\'::jsonb').first()[0])
    self.assertEqual(True, db.session.execute('SELECT \'{"context": {"team_id": 1, "project_id": 2, "project_media_id": 3}}\'::jsonb @> \'{}\'::jsonb').first()[0])

  def test_context_query(self):
    self.assertEqual(True, add_phash(1, 2, 'ext', 'url', {"context": {"team_id": 1, "project_id": 2, "project_media_id": 3}}))
    self.assertEqual(1, len(search_by_phash(2, 6, 1, 0, {})))
    self.assertEqual(0, len(search_by_phash(2, 6, 1, 0, {"context": {"project_id": 3}})))

if __name__ == '__main__':
  unittest.main()
