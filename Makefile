docker-local-build:
	docker-compose -f ./server-config/local/docker-compose.yml build
docker-local-run:
	docker-compose -f  ./server-config/local/docker-compose.yml up --build
docker-local-down:
	docker-compose -f  ./server-config/local/docker-compose.yml down
docker-local-run-tests:
	docker-compose -f ./server-config/local/docker-compose.yml run back pytest /www/src/tests
docker-local-loaddata:
	docker-compose -f ./server-config/local/docker-compose.yml exec back python ./src/manage.py loaddata db.json --settings=config.settings.local
docker-local-migrate:
	docker  exec -it python /www/src/manage.py migrate --settings=config.settings.local --no-input 
docker-local-makemigrations:
	docker  exec -it python /www/src/manage.py makemigrations --settings=config.settings.local --no-input
