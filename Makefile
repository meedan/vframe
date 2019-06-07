.PHONY: run test env
env:
	conda activate vframe
run: env
	cd api && python api/cli_flask.py run --host=0.0.0.0
test: env
	cd api && FLASK_ENV=test DB_NAME=vframe_test coverage run manage.py test
requirements: env
	pip freeze > requirements.txt
	conda-env export > environment.yml
