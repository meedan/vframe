import os
import glob
import time
import pandas as pd

from PIL import Image

from sqlalchemy import create_engine, Table, Column, String, Integer, BigInteger, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import app_cfg

from app.utils.im_utils import compute_phash_int
from app.utils.file_utils import sha256

connection_url = "mysql+mysqlconnector://{}:{}@{}/{}?charset=utf8mb4".format(
  os.getenv("DB_USER"),
  os.getenv("DB_PASS"),
  os.getenv("DB_HOST"),
  os.getenv("DB_NAME")
)

loaded = False
engine = create_engine(connection_url, encoding="utf-8", pool_recycle=3600)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class FileTable(Base):
  """Table for storing various hashes of images"""
  __tablename__ = os.getenv("DB_TABLE") or 'files'
  id = Column(Integer, primary_key=True)
  sha256 = Column(String(64, convert_unicode=True), nullable=False, unique=True)
  phash = Column(BigInteger, nullable=False, index=True)
  ext = Column(String(4, convert_unicode=True), nullable=False)
  url = Column(String(255, convert_unicode=True), nullable=False)
  def toJSON(self):
    return {
      'id': self.id,
      'sha256': self.sha256,
      'phash': self.phash,
      'ext': self.ext,
      'url': self.url,
    }

Base.metadata.create_all(engine)


def search_by_phash(phash, threshold=6, limit=1, offset=0):
  """Search files for a particular phash"""
  # connection = engine.connect()
  session = Session()
  cmd = """
    SELECT files.*, BIT_COUNT(phash ^ :phash) 
    AS hamming_distance FROM files 
    HAVING hamming_distance < :threshold 
    ORDER BY hamming_distance ASC 
    LIMIT :limit
    OFFSET :offset
  """
  matches = session.execute(text(cmd), { 'phash': phash, 'threshold': threshold, 'limit': limit, 'offset': offset }).fetchall()
  keys = ('id', 'sha256', 'phash', 'ext', 'url', 'score')
  results = [ dict(zip(keys, values)) for values in matches ]
  session.close()
  return results

def search_by_hash(hash):
  session = Session()
  match = session.query(FileTable).filter(FileTable.sha256 == hash)
  result = match.first()
  session.close()
  return result

def add_phash(sha256=None, phash=None, ext=None, url=None):
  """Add a file to the table"""
  rec = FileTable(sha256=sha256, phash=phash, ext=ext, url=url)
  session = Session()
  session.add(rec)
  session.commit()
  session.flush()


def add_phash_by_filename(path):
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

  add_phash(sha256=hash, phash=phash, ext=ext, url=path)
