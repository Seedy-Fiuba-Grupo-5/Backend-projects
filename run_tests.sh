#!/bin/sh
echo "[RUN_TESTS] waiting for postgres to start ..."
docker-compose exec service_projects_web bash -c 'while ! nc -z service_projects_db 5432; do sleep 1; done;'

echo "[RUN_TESTS] Running tests ..."
docker-compose exec service_projects_web pytest "dev/tests" --cov="prod" -p no:warnings

echo "[RUN_TESTS] Running flake8 inside all folders"
docker-compose exec service_projects_web flake8 prod
