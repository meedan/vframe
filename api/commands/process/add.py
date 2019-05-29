"""
Add a file to the database
"""

import click

from app.models.sql_factory import add_phash_by_filename

@click.command()
@click.option('-i', '--input', 'opt_fn',
  required=True,
  help="File to add (gif/jpg/png)")
@click.option('-u', '--upload', 'opt_upload', is_flag=True,
  help='Whether to upload this file to S3')
@click.pass_context
def cli(ctx, opt_fn, opt_upload):
  """
  Add a single file
  """
  print('Adding a file...')
  add_phash_by_filename(opt_fn)
