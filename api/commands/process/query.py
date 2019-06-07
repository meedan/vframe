"""
Query the database with a test set
"""

import click

from app.settings import app_cfg

@click.command()
@click.option('-i', '--input', 'opt_input',
  required=True,
  type=click.Path(),
  help='Input directory of images')
@click.option('-e', '--ext', 'opt_ext', default='jpeg',
  type=click.Choice(app_cfg.IMAGE_EXTS),
  help='Image extension to glob')
@click.pass_context
def cli(ctx, opt_input, opt_ext):
  """
  Query the database with a test set
  """

  import os
  from os.path import join
  import glob
  from pathlib import Path
  import time

  from PIL import Image
  from tqdm import tqdm

  from app.models.sql_factory import search_by_phash, search_by_hash
  from app.utils.im_utils import compute_phash_int
  from app.utils.file_utils import sha256
  from app.utils import logger_utils

  log = logger_utils.Logger.getLogger()

  if Path(opt_input).is_file():
    files = [opt_input]
  else:
    files = sorted(glob.iglob(join(opt_input, f'*.{opt_ext}')))

  log.info(f'Querying {len(files)} files')

  if not len(files):
    log.warn(f'No files found. Did you mean to scan for ".{opt_ext}" files?')
    return

  for fn in tqdm(files):
    im = Image.open(fn).convert('RGB')
    phash = compute_phash_int(im)

    hash_s256 = sha256(fn)

    phash_match = search_by_phash(phash)
    hash_match = search_by_hash(hash_s256)

    hash_result = 'NO'
    if hash_match:
      hash_result = 'YES'

    phash_result = 'NO'
    if len(phash_match):
      phash_result = 'YES, score={}'.format(phash_match[0]['score'])

    log.info("{} - hash={}, phash={}".format(Path(fn).name, hash_result, phash_result))

"""
Debugging:
timeout error occurs from the `search_by_hash`

sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30 (Background on this error at: http://sqlalche.me/e/3o7r)
"""