#!/bin/bash
set -e

# Start Redis (not yet needed)
#./wait-for-it/wait-for-it.sh mysql:3306 && ./wait-for-it/wait-for-it.sh redis:6379

# Init conda env
source activate vframe

# build JS
npm i && npm run buildDev

# run Flask app
cd check && python cli_flask.py run --host=0.0.0.0
