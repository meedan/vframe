"""
Generate a test report from a directory of images
This demo does not use SQL storage

"""

from pathlib import Path

import click

@click.command('')
@click.option('-i', '--input', 'opt_fp_in', required=True,
  help='Path to input dir')
@click.option('-o', '--output', 'opt_fp_out', required=True,
  help='Path to output directory')
@click.option('--recursive', 'opt_recursive', is_flag=True,
  help='Recursive globbing')
@click.option('-t', '--thresh', 'opt_thresh', default=3,
  help='Perceptual hash threshold')
@click.option('--slice', 'opt_slice', type=(int, int), default=(None, None))
@click.pass_context
def cli(ctx, opt_fp_in, opt_fp_out, opt_recursive, opt_thresh, opt_slice):
  """Deduplicate images for report generation"""

  # ------------------------------------------------
  # imports
  import sys
  from os.path import join
  from glob import glob

  import pandas as pd
  from tqdm import tqdm
  import numpy as np
  import cv2 as cv
  import imagehash

  from app.utils import logger_utils, im_utils, file_utils
  
  log = logger_utils.Logger.getLogger()
  log.info(f'De-duplicating: {opt_fp_in}')

  # get list of all images
  fp_ims = glob(join(opt_fp_in, '*'))
  log.info(len(fp_ims))
  
  exts = ['.jpg', '.png', '.jpeg']
  fp_ims = [x for x in fp_ims if Path(x).suffix in exts]
  if opt_slice:
    fp_ims = fp_ims[opt_slice[0]:opt_slice[1]]

  log.info(f'Processing {len(fp_ims):,} images')

  # Create image meta objects
  ims_meta = {}
  log.info('Computing sha256 and perceptual hashes...')
  for fp_im in tqdm(fp_ims):
    sha256 = file_utils.sha256(fp_im)
    im = cv.imread(fp_im)
    im_hash = im_utils.compute_phash(im) # uses PIL
    ims_meta[sha256] = {
      'imhash': im_hash,
      'filepath': fp_im,
      'fname': Path(fp_im).name,
      'sha256': sha256,
      'duplicate': None,
      }

  # Deduplicate the list of images
  log.info('Deduplicating images...')
  duplicates = []
  names_added = []
  for sha256_a, im_obj_a in tqdm(ims_meta.copy().items()):  
    for sha256_b, im_obj_b in ims_meta.copy().items():
      if sha256_a == sha256_b or im_obj_b['fname'] in names_added:
        continue
      d = abs(im_obj_a['imhash'] - im_obj_b['imhash'])
      if d <= opt_thresh:
        # mark B as a duplicate of A
        #ims_meta[sha256_b]['duplicate'] = sha256_a
        duplicates.append({'sha256_a': sha256_a, 'fname_a': im_obj_a['fname'], 
          'sha256_b': sha256_b, 'fname_b': im_obj_b['fname'], 'score': d})
        ims_meta.pop(sha256_b)
        names_added.append(im_obj_a['fname'])

  n_dupes = sum(1 for k,v in ims_meta.items() if v['duplicate'] is not None) 
  log.info(f'Found {n_dupes}')

  df_items = pd.DataFrame.from_dict(duplicates)
  file_utils.ensure_dir(opt_fp_out)
  log.info(f'Writing: {opt_fp_out}')
  df_items.to_csv(opt_fp_out, index=False)