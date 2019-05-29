# --------------------------------------------------------
# wrapper for flask CLI API
# NB: python cli_flask.py run
# --------------------------------------------------------

import click

from flask.cli import FlaskGroup
from app.server.create import create_app

cli = FlaskGroup(create_app=create_app)

# --------------------------------------------------------
# Entrypoint
# --------------------------------------------------------
if __name__ == '__main__':
    cli()
