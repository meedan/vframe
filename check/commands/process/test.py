"""
Test the API
"""

import click

mime_types = {
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
}

@click.command()
@click.option('-i', '--input', 'opt_input_fn',
  required=True,
  help="Image to test the API with")
@click.pass_context
def cli(ctx, opt_input_fn):
  """
  Query the API with a test image
  """
  import os
  import glob
  import requests
  
  from app.utils import logger_utils

  log = logger_utils.Logger.getLogger()

  with open(opt_input_fn, 'rb') as f:
    fn = os.path.basename(opt_input_fn)
    fpart, ext = os.path.splitext(fn)
    if ext not in mime_types:
      log.info("Invalid filetype: {}".format(ext))

    query = [
      ('q', (fn, f, mime_types[ext]))
    ]

    log.info("Testing match API")
    r = requests.post('http://0.0.0.0:5000/api/v1/match', files=query)
    log.info(r.json())
