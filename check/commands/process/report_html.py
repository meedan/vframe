"""
Generate a test report from a directory of images
This demo does not use SQL storage

"""

from pathlib import Path

import click

@click.command('')
@click.option('--csv', 'opt_fp_in_csv', required=True,
  help='Path to input CSV')
@click.option('--images', 'opt_fp_in_img', required=True,
  help='Path to images')
@click.option('-o', '--output', 'opt_fp_out_dir', type=click.Path(file_okay=False, dir_okay=True),
  help='Path to output directory')
@click.pass_context
def cli(ctx, opt_fp_in_csv, opt_fp_in_img, opt_fp_out_dir):
  """Generate HTML report from deduped images"""

  # ------------------------------------------------
  # imports
  import sys
  from os.path import join
  from glob import glob

  import pandas as pd
  from tqdm import tqdm
  import jinja2
  from flask import url_for
  import shutil

  from app.utils import logger_utils, im_utils, file_utils
  
  log = logger_utils.Logger.getLogger()
  log.info(f'Generating HTML report from: {opt_fp_in_csv}')


  template_loader = jinja2.FileSystemLoader(searchpath="./static/")
  template_env = jinja2.Environment(loader=template_loader)
  TEMPLATE_FILE = "perceptual_hash_report.html"
  template = template_env.get_template(TEMPLATE_FILE)

  # create project output dir
  fp_out_dir_assets = join(opt_fp_out_dir, 'assets')
  fp_out_dir_images = join(opt_fp_out_dir, 'images')
  
  file_utils.ensure_dir(opt_fp_out_dir)
  file_utils.ensure_dir(fp_out_dir_assets)
  file_utils.ensure_dir(fp_out_dir_images)
  
  df_dupes = pd.read_csv(opt_fp_in_csv)
  image_groups = df_dupes.groupby('fname_a')

  log.info(f'Saving HTML report to: {opt_fp_out_dir}')
  # im_objs = df_dupes.to_records('dict')
  fp_out_html = join(opt_fp_out_dir, 'index.html')
  with open(fp_out_html, 'w') as fp:
    html_text = template.render(image_groups=image_groups, 
      dir_ims=Path(fp_out_dir_images).name, dir_assets=Path(fp_out_dir_assets).name)
    fp.write(html_text)
  
  # copy css
  fp_src = 'static/assets/css.css'
  fp_dst = join(fp_out_dir_assets, Path(fp_src).name)
  shutil.copy(fp_src, fp_dst)

  # copy images
  for fname_a, image_group in image_groups:
    # get image a
    for df_im in image_group.itertuples():
      # image a
      fp_src = join(opt_fp_in_img, df_im.fname_a)
      fp_dst = join(fp_out_dir_images, df_im.fname_a)
      shutil.copy(fp_src, fp_dst)
      # image b
      fp_src = join(opt_fp_in_img, df_im.fname_b)
      fp_dst = join(fp_out_dir_images, df_im.fname_b)
      shutil.copy(fp_src, fp_dst)