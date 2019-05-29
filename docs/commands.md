# Commands

To run any of the commands, first activate the appropriate conda environment, e.g. `conda activate vframe`.

The scripts can all be found in the `api` folder at the base of the repo.  Further info on the scripts can be found by adding the CLI argument ``--help``


## Production commands

## cli_phash.py import

Import a (local) folder of images.  These images will be indexed and should be accessible from the web (i.e. put them in `static`)

- `--input` - Input glob, i.e. `'static/sample_set_test_01/images/*'` - remember to quote the glob
- `--threshold` - Similarity threshold for deuping (default is 6)

## cli_phash.py import_csv

Given a CSV file of image URLs, import them into the database.

- `--input` - Input CSV file
- `--base_href` - Base HREF to prepend to all URLs (default is empty string)
- `--field` - Field in the CSV which contains the URL


## Development commands

## cli_flask.py run

Runs the development Flask server.

## cli_phash.py add

Add a single (local) file to the database.

## cli_phash.py dedupe

Dedupe a (local) folder of images.

## cli_phash.py drop

Drop the database tables (must pass `--force`).

## cli_phash.py query

Query the database with a test set of (local) images.

## cli_phash.py report

Dedupe a folder of images and generate a similarity report.

## cli_phash.py report_html

Dedupe a folder of images and generate a similarity report (as HTML).

## cli_phash.py test

Test the match API by uploading a local image.  Image will not be stored in the database.
