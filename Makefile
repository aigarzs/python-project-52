start:
	poetry run python manage.py runserver


dev:
	poetry run python manage.py runserver


django-shell:
	poetry run python manage.py shell

check:
	poetry run flake8 task_manager tests
	poetry run python3 manage.py test --keepdb tests/

makemessages:
	poetry run django-admin makemessages -l en
	poetry run django-admin makemessages -l ru
	poetry run django-admin makemessages -l lv

compilemessages:
	poetry run django-admin compilemessages
