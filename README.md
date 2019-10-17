# vFrame Check API

[![Build Status](https://travis-ci.org/meedan/vframe.svg?branch=develop)](https://travis-ci.org/meedan/vframe)

The vFrame Check API Service uses perceptual hash to disambiguate similar images, as well as provide an image-based search engine.

## Path Structure

- `api` - Python app / `click` cli.
- `client` - React frontend
- `docs` - Documentation
- `nginx` - Sample configuration files for deployment

## Quick Start

- Copy `.env_file.example` to `.env_file` and adjust accordingly (defaults are fine)
- `docker-compose build`
- `docker-compose up`
- Demonstration page http://0.0.0.0:5000/static/demo.html
- `docker-compose exec vframe bash`
- `conda activate vframe`
- `cd api && FLASK_ENV=test DB_NAME=vframe_test coverage run manage.py test`

## Importing Images

The initial dataset can be hosted locally for now - make sure files are accessible inside `api/static/`.  These paths will be added directly to the dataset. These 3 examples all run the same command:

```
cd api
python cli_proc.py import
python cli_proc.py import --input path/to/your/images/ --ext jpg
python cli_proc.py import --i path/to/your/images/ --e jpg
```

Alternatively, import a CSV of image URLs, hosted externally.  The images will be temporarily fetched and processed.

```
cd api
python cli_proc.py import_csv -i ../data/url_test.csv --field url
```

## Production

The production server runs under NGINX using uWSGI.  We set up uWSGI as a systemctl service:

```
sudo cp nginx/uwsgi.service /etc/systemd/system/vframe_check.service
sudo systemctl start vframe_check.service
```

Please modify the example config file.  Update where appropriate and please do grab a cert:

```
sudo cp nginx/nginx.config /etc/nginx/sites-available/vframe-check.example.com
sudo ln -s /etc/nginx/sites-available/check.example.com /etc/nginx/sites-enabled/vframe-check.example.com
sudo nginx -t
sudo service nginx restart
sudo certbot --nginx
```

Finally, build the Javascript frontend for production:

```
npm run build
```

## Documentation

Documentation for the various commands and API endpoints can be found in the `docs` folder.
