import os
from os.path import join
import logging
import collections
from dotenv import load_dotenv

from app.settings import types
from app.utils import click_utils
from pathlib import Path

# -----------------------------------------------------------------------------
# click settings
# -----------------------------------------------------------------------------
DIR_COMMANDS_PROCESS = 'commands/process'

# -----------------------------------------------------------------------------
# File I/O
# -----------------------------------------------------------------------------
IMAGE_EXTS = ['jpg', 'jpeg', 'png']

# -----------------------------------------------------------------------------
# S3 storage
# -----------------------------------------------------------------------------
S3_ROOT_URL = 's3://check-vframe/v1/'
S3_METADATA_URL = join(S3_ROOT_URL, 'metadata')
S3_HTTP_URL = 'https://check-vframe.nyc3.digitaloceanspaces.com/v1/'
S3_HTTP_METADATA_URL = join(S3_HTTP_URL, 'metadata')

# -----------------------------------------------------------------------------
# Celery
# -----------------------------------------------------------------------------
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# -----------------------------------------------------------------------------
# Logging options exposed for custom click Params
# -----------------------------------------------------------------------------
LOGGER_NAME = 'app'
LOGLEVELS = {
  types.LogLevel.DEBUG: logging.DEBUG,
  types.LogLevel.INFO: logging.INFO,
  types.LogLevel.WARN: logging.WARN,
  types.LogLevel.ERROR: logging.ERROR,
  types.LogLevel.CRITICAL: logging.CRITICAL
}
LOGLEVEL_OPT_DEFAULT = types.LogLevel.DEBUG.name
#LOGFILE_FORMAT = "%(asctime)s: %(levelname)s: %(message)s"
#LOGFILE_FORMAT = "%(levelname)s:%(name)s: %(message)s"
#LOGFILE_FORMAT = "%(levelname)s: %(message)s"
#LOGFILE_FORMAT = "%(filename)s:%(lineno)s  %(funcName)s()  %(message)s"
# colored logs
"""
black, red, green, yellow, blue, purple, cyan and white.
{color}, fg_{color}, bg_{color}: Foreground and background colors.
bold, bold_{color}, fg_bold_{color}, bg_bold_{color}: Bold/bright colors.
reset: Clear all formatting (both foreground and background colors).
"""
LOGFILE_FORMAT = "%(log_color)s%(levelname)-8s%(reset)s %(cyan)s%(filename)s:%(lineno)s:%(bold_cyan)s%(funcName)s() %(reset)s%(message)s"

LogLevelVar = click_utils.ParamVar(types.LogLevel)

# -----------------------------------------------------------------------------
# Filesystem settings
# hash trees enforce a maximum number of directories per directory
# -----------------------------------------------------------------------------
ZERO_PADDING = 6  # padding for enumerated image filenames
#FRAME_NAME_ZERO_PADDING = 6  # is this active??
CKPT_ZERO_PADDING = 9
HASH_TREE_DEPTH = 3
HASH_BRANCH_SIZE = 3

# -----------------------------------------------------------------------------
# .env config for keys
# -----------------------------------------------------------------------------
# DIR_DOTENV = join(DIR_APP, '.env')
load_dotenv() # dotenv_path=DIR_DOTENV)
