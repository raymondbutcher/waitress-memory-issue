server:
	waitress-serve app:api

load:
	locust --host http://0.0.0.0:8080 --no-web --clients 10 --hatch-rate 1

check:
	curl http://0.0.0.0:8080/check
