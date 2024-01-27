make:
	python3 manage.py makemigrations
	python3 manage.py migrate

makeclary:
	celery -A root worker -l info
	celery -A root flower --port=5555