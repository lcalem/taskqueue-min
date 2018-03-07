PROJECT_NAME := taskqueue


docker-%:
	docker build -f docker/dockerfiles/Dockerfile.$* -t $(PROJECT_NAME)_$* .

up_tests:
	docker-compose -f docker/compose/docker-compose-tests.yml down
	docker-compose -f docker/compose/docker-compose-tests.yml up -d
	docker exec -it compose_test_1 bash

down_tests:
	docker-compose -f docker/compose/docker-compose-tests.yml down