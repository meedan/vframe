"""
Drop the database (useful when testing)
"""

import click

@click.command()
@click.option('-f', '--force', 'opt_force', is_flag=True,
  help='Actually drop the database')
@click.pass_context
def cli(ctx, opt_force):
  """
  Drop the database
  """
  import glob

  from app.models.sql_factory import Base, engine
  from app.utils import logger_utils

  log = logger_utils.Logger.getLogger()

  if not opt_force:
    log.warn('Are you sure?')
    log.info('Use the --force flag to drop the database.')
  else:
    log.info('Dropping the database!')
    Base.metadata.drop_all(engine)
