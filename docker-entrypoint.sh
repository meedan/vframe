#!/bin/bash
set -e
source activate vframe
npm i && npm run build:dev
cd api && python cli_flask.py run --host=0.0.0.0
