
docker-image:
	docker build -t dns-restful .

docker-run: docker-image
	docker run -d -p 9401:9401 --env-file .env dns-restful