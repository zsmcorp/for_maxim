start:
	docker-compose up --build -d
stop:
	docker-compose stop
restart:
	docker-compose restart
logs:
	docker-compose logs -f
kill:
	docker-compose kill
clear:
	docker system prune --all --volumes
container:
	docker container ls -a
admin:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python3 app_api/manage.py createsuperuser --noinput || true
make-trans:
	django-admin makemessages -l ru -e py -e html -i venv
compile-trans:
	django-admin compilemessages --exclude venv
snyk:
	cd ../app_api && snyk test --docker alpine:3.14 --file=Dockerfile