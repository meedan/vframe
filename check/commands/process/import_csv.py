"""
Import a CSV of URLs
"""

import click

@click.command()
@click.option('-i', '--input', 'opt_input_fn',
  required=True,
  help="Input path to CSV")
@click.option('-b', '--base_url', 'opt_base_url',
  default='',
  help="Base HREF for the URLs in the CSV. Optional; default is empty string ''")
@click.option('--field', 'opt_field',
  required=False,
  default="url",
  help="Field in CSV containing URL")
@click.pass_context
def cli(ctx, opt_input_fn, opt_base_url, opt_field):
  """
  Import a CSV of image URLS formatted  as:
  """
  """
  | url |
  | --- |
  | https://site.com/image1.jpg |
  | https://site.com/image2.jpg |
  
  (markdown syntax only used for example)

  alternatively, use a base ahref and only the image name:
  | url |
  | --- |
  | image1.jpg |
  | image2.jpg |
  
  --base_url "https://site.com/"

  """
  
  import os
  import glob
  import io
  import random

  from PIL import Image

  from app.models.sql_factory import add_phash
  from app.utils.im_utils import compute_phash_int
  from app.utils.file_utils import load_csv, sha256_stream
  from app.utils.process_utils import parallelize
  from app.server.api import fetch_url
  from app.settings import app_cfg
  from app.utils import logger_utils

  log = logger_utils.Logger.getLogger()

  def add_url(url):
    fname, ext = os.path.splitext(url)
    if ext not in app_cfg.IMAGE_EXTS:
      return
    ext = ext[1:]
    try:
      raw, im = fetch_url(url)
    except:
      log.warn('404 {}'.format(url))
      return
    log.info(url)
    phash = compute_phash_int(im)
    hash = sha256_stream(io.BytesIO(raw))
    add_phash(sha256=hash, phash=phash, ext=ext, url=url)

  rows = load_csv(opt_input_fn)
  urls = [opt_base_url + row['url'] for row in rows]
  random.shuffle(urls)
  log.info('Parallelizing import')
  parallelize(urls, add_url)

