run:
	docker run --name transloc-db -e POSTGRES_PASSWORD=translocPassword -d -p 5431:5432 postgres

start:
	docker start transloc-db

stop:
	docker stop transloc-db