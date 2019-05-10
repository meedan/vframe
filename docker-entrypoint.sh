#!/bin/bash
set -e
./wait-for-it/wait-for-it.sh mysql:3306 && ./wait-for-it/wait-for-it.sh redis:6379
npm i && npm run buildDev
cd check && python cli_flask.py run --host=0.0.0.0
