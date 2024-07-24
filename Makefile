start:
	poetry run python manage.py runserver


dev:
	poetry run python manage.py runserver


django-shell:
	poetry run python manage.py shell


makemessages:
	poetry run django-admin makemessages -l en
	poetry run django-admin makemessages -l ru
	poetry run django-admin makemessages -l lv

compilemessages:
	poetry run django-admin compilemessages
