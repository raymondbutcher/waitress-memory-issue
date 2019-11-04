server-8k:
	waitress-serve --outbuf-overflow=8192 app:api

server-16k:
	waitress-serve --outbuf-overflow=16384 app:api

load:
	locust --host http://0.0.0.0:8080 --no-web --clients 10 --hatch-rate 1

check:
	curl http://0.0.0.0:8080/check
