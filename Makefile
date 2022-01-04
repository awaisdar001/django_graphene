run:
	python manage.py runserver 127.0.0.1:8000

requirements:
	pip install -r requirements.txt

test:
	pytest -v

migrate:
	python manage.py migrate

load:
	python manage.py loaddata ./scheduler/meeting_scheduler/factories/users.json

setup: requirements migrate load

