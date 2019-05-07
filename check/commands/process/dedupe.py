"""
Dedupe a folder of images (uses phash directly, does not use database)
"""

import click

@click.command()
@click.option('-i', '--input', 'opt_input_glob',
  required=True,
  default='static/sample_set_test_01/images/',
  type=click.Path(exists=True),
  help='Path to directory of images')
@click.option('-o', '--output', 'opt_output_fn',
  required=False,
  help="Output filename")
@click.option('-t', '--threshold', 'opt_threshold',
  required=True,
  default=4,
  type=click.IntRange(0, 20, clamp=True),
  show_default=True,
  help="Threshold for hamming distance comparison (0-64)")
@click.pass_context
def cli(ctx, opt_input_glob, opt_output_fn, opt_threshold, opt_ext):
  """
  Dedupe a folder of images
  """
  
  import os
  import glob

  from PIL import Image

  from app.utils.im_utils import compute_phash
  from app.utils.file_utils import write_json, sha256
  from app.utils import logger_utils

  log = logger_utils.Logger.getLogger()

  seen = []
  total = 0

  for fn in tqdm(sorted(glob.iglob(join(opt_input_glob, f'*.{opt_ext}')))):
    total += 1
    im = Image.open(fn).convert('RGB')
    phash = compute_phash(im)
    if is_phash_new(fn, phash, seen, opt_threshold):
      hash = sha256(fn)
      fpart, ext = os.path.splitext(fn)
      ext = ext[1:]
      seen.append({
        'sha256': hash,
        'phash': phash,
        'fn': fn,
        'ext': ext,
      })
  if opt_output_fn:
    write_json(seen, opt_output_fn)
  log.info("checked {} files, found {} unique".format(total, len(seen)))


def is_phash_new(fn, phash, seen, opt_threshold):
  for item in seen:
    diff = item['phash'] - phash
    if diff < opt_threshold:
      log.info("{} === {} (diff: {})".format(fn, item['fn'], diff))
      return False
  return True
