import os
import glob
import time
import json
import pandas as pd

from PIL import Image

import sqlalchemy
from sqlalchemy import create_engine, Table, Column, String, Integer, BigInteger, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.schema import DDL
from sqlalchemy.dialects.postgresql import JSONB

from app.settings import app_cfg

from app.utils.im_utils import compute_phash_int
from app.utils.file_utils import sha256

connection_url = "postgresql+psycopg2://{}:{}@{}/{}?client_encoding=utf8".format(
  os.getenv("DB_USER"),
  os.getenv("DB_PASS"),
  os.getenv("DB_HOST"),
  os.getenv("DB_NAME")
)

loaded = False
engine = create_engine(connection_url, encoding="utf-8", pool_recycle=3600)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Create database if needed.
if not database_exists(engine.url):
  create_database(engine.url)

# Create the bit_count function.
# https://stackoverflow.com/a/30397705/209184
# https://stackoverflow.com/q/46280722/209184
sqlalchemy.event.listen(
    Base.metadata,
    'before_create',
    DDL("""
      CREATE OR REPLACE FUNCTION bit_count(value bigint)
      RETURNS integer
      AS $$ SELECT length(replace(value::bit(64)::text,'0','')); $$
      LANGUAGE SQL IMMUTABLE STRICT;
    """)
)

class FileTable(Base):
  """Table for storing various hashes of images"""
  __tablename__ = os.getenv("DB_TABLE") or 'files'
  id = Column(Integer, primary_key=True)
  sha256 = Column(String(64, convert_unicode=True), nullable=False, unique=True)
  phash = Column(BigInteger, nullable=False, index=True)
  ext = Column(String(4, convert_unicode=True), nullable=False)
  url = Column(String(255, convert_unicode=True), nullable=False)
  context = Column(JSONB(), default={}, nullable=False, index=True)
  def toJSON(self):
    return {
      'id': self.id,
      'sha256': self.sha256,
      'phash': self.phash,
      'ext': self.ext,
      'url': self.url,
      'context': self.context
    }

Base.metadata.create_all(engine)

def search_by_phash(phash, threshold=6, limit=1, offset=0, filter={}):
  """Search files for a particular phash"""
  # connection = engine.connect()
  session = Session()

  cmd = """
    SELECT * FROM (
      SELECT files.*, BIT_COUNT(phash # :phash)
      AS hamming_distance FROM files
    ) f
    WHERE hamming_distance < :threshold
    AND context @> (:filter)::jsonb
    ORDER BY hamming_distance ASC
    LIMIT :limit
    OFFSET :offset
  """
  matches = session.execute(text(cmd), {
    'phash': phash,
    'threshold': threshold,
    'limit': limit,
    'offset': offset,
    'filter': json.dumps(filter)
  }).fetchall()
  keys = ('id', 'sha256', 'phash', 'ext', 'url', 'context', 'score')
  results = [ dict(zip(keys, values)) for values in matches ]
  session.close()
  return results

def search_by_hash(hash):
  session = Session()
  match = session.query(FileTable).filter(FileTable.sha256 == hash)
  result = match.first()
  session.close()
  return result

def add_phash(sha256=None, phash=None, ext=None, url=None, context={}):
  """Add a file to the table"""
  rec = FileTable(sha256=sha256, phash=phash, ext=ext, url=url, context=context)
  session = Session()
  try:
    session.add(rec)
    session.commit()
    session.flush()
  except sqlalchemy.exc.IntegrityError:
    session.rollback()
    return False

  return True

def add_phash_by_filename(path, context={}):
  """Add a file by filename, getting all the necessary attributes"""
  print(path)
  if not os.path.exists(path):
    print("File does not exist")
    return

  dir, fn = os.path.split(path)
  root, ext = os.path.splitext(fn)
  ext = ext.strip('.')
  if ext not in app_cfg.IMAGE_EXTS:
    print("Not an image file")
    return

  im = Image.open(path).convert('RGB')
  phash = compute_phash_int(im)
  hash = sha256(path)
  add_phash(sha256=hash, phash=phash, ext=ext, url=path, context=context)
