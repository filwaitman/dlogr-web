test:
	./manage.py collectstatic --no-input -v0
	flake8 . --max-line-length=120 --exclude=.git,*/static/*
	coverage run --source='main,dlogr_web' --omit='*tests*,*commands*,*migrations*,*admin*,*config*,*wsgi*,*apps*' ./manage.py test main${ARGS}
	coverage report

serve:
	./manage.py runserver${ARGS}

shell:
	./manage.py shell${ARGS}
