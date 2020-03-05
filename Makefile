.PHONY: run build kill tty

build:
	docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_bcrypt docker" -t opendatabs/docker-airflow .

run: build
	docker-compose -f docker-compose.yml up -d
	@echo airflow running on http://localhost:8080

kill:
	@echo "Killing docker-airflow containers"
	docker kill $(shell docker ps -q --filter ancestor=opendatabs/docker-airflow)

tty:
	docker exec -i -t $(shell docker ps -q --filter ancestor=opendatabs/docker-airflow) /entrypoint.sh /bin/bash