docker-build:
	docker build -t lukaswire/anthe .

docker-run: docker-build
	docker run --rm -p 8080:8080 lukaswire/anthe

docker-deploy: docker-build
	docker push lukaswire/anthe