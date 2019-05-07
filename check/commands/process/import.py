"""
Import a folder of images, deduping them first
"""

import click

from app.settings import app_cfg

valid_exts = ['.gif', '.jpg', '.jpeg', '.png']

@click.command()
@click.option('-i', '--input', 'opt_input_glob',
  required=True,
  default='static/sample_set_test_01/images/',
  type=click.Path(exists=True),
  help='Path to directory of images')
@click.option('-t', '--threshold', 'opt_threshold',
  required=True,
  default=4,
  type=click.IntRange(0, 20, clamp=True),
  show_default=True,
  help="Threshold for hamming distance comparison (0-64)")
@click.option('-e', '--ext', 'opt_ext', default='jpeg',
  type=click.Choice(app_cfg.IMAGE_EXTS),
  help='Image extension to glob')
@click.option('--dry-run', 'opt_dry_run', is_flag=True,
  help='Run a test and do not import hashes to mysql')
@click.pass_context
def cli(ctx, opt_input_glob, opt_threshold, opt_ext, opt_dry_run):
  """
  Import a folder of images, deduping them first
  """
  
  import os
  from os.path import join
  import glob
  from pathlib import Path

  from PIL import Image
  from tqdm import tqdm

  from app.models.sql_factory import add_phash
  from app.utils.im_utils import compute_phash, phash2int
  from app.utils.file_utils import write_json, sha256
  from app.utils import logger_utils


  log = logger_utils.Logger.getLogger()

  if opt_dry_run:
    log.info('Dry run. Image hashes will not be imported to mysql')

  seen = []
  total = 0
  log.info(f'Scanning for files in: {opt_input_glob}')

  for fn in tqdm(sorted(glob.iglob(join(opt_input_glob, f'*.{opt_ext}')))):
    ext = Path(fn).suffix[1:]
    total += 1
    im = Image.open(fn).convert('RGB')
    phash = compute_phash(im)
    if is_phash_new(fn, phash, seen, opt_threshold):
      hash = sha256(fn)
      url = '/' + fn
      seen.append({
        'sha256': hash,
        'phash': phash,
        'fn': fn,
      })
      if not opt_dry_run:
        add_phash(sha256=hash, phash=phash2int(phash), ext=ext, url=url)
  log.info("checked {} files, found {} unique".format(total, len(seen)))

def is_phash_new(fn, phash, seen, opt_threshold):
  for item in seen:
    diff = item['phash'] - phash
    if diff < opt_threshold:
      return False
  return True
