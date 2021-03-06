db:
	docker-compose up -d db

add-migration: # add-migration M="some nice name"
	 flask db migrate -m "$$M"

migrate-db:
	flask db upgrade

docker-build:
	docker build -t lukaswire/anthe .

docker-run: docker-build
	docker run --rm -p 8080:8080 lukaswire/anthe

publish: docker-build
	docker push lukaswire/anthe