# VFRAME Check API

The VFRAME Check API Service uses perceptual hash to disambiguate similar images, as well as provide an image-based search engine.

## Path Structure

- `check` - Python app / `click` cli.
- `client` - React frontend
- `docs` - Documentation
- `nginx` - Sample configuration files for deployment

## Quick Start


Install nginx, MySQL

```
apt install git nginx mysql-server mysql-client
mysql_secure_installation
mysql -u root -p
```


Create MySQL user:

```
CREATE DATABASE vframe_check;
CREATE USER 'vframe_check'@'localhost' IDENTIFIED BY 'some_new_password';
GRANT ALL PRIVILEGES ON vframe_check.* to 'vframe_check'@'localhost';
```

Create a file called `.env` and put it inside the `check` folder at the root of this repo:

```
DB_HOST=localhost
DB_NAME=vframe_check
DB_USER=vframe_check
DB_PASS=some_new_password
```

Install Conda or Miniconda, then install the `vframe_check` conda environement:

```
conda env create -f environment.yml
```

At this point, try to run the CLI processor. It should output a list of commands. Check for any `ImportErrors`.

```
python cli_proc.py
```


## Importing Images

The initial dataset can be hosted locally for now - make sure files are accessible inside `check/static/`.  These paths will be added directly to the dataset. These 3 examples all run the same command:

```
python cli_proc.py import
python cli_proc.py import --input path/to/your/images/ --ext jpg
python cli_proc.py import --i path/to/your/images/ --e jpg
```

Alternatively, import a CSV of image URLs, hosted externally.  The images will be temporarily fetched and processed.

```
python cli_proc.py import_csv -i ..data/url_test.csv --field url
```

## Development

Start watching the frontend for changes:

```
npm run watch
```

Run the development server:

```
cd check
python cli_flask.py run
```

Demonstration page: http://0.0.0.0:5000/static/demo.html

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
