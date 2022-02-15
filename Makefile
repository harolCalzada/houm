docker-local-build:
	docker-compose -f ./server-config/local/docker-compose.yml build
docker-local-run:
	docker-compose -f  ./server-config/local/docker-compose.yml up
docker-local-down:
	docker-compose -f  ./server-config/local/docker-compose.yml down
docker-local-migrate:
	docker  exec -it python /www/src/manage.py migrate --settings=config.settings.local --no-input 
docker-local-makemigrations:
	docker  exec -it python /www/src/manage.py makemigrations --settings=config.settings.local --no-input
