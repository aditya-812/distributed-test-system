.PHONY: help install build up down run test logs ps clean setup health load-test

help:
	@echo "Usage:"
	@echo "  make setup      Run setup script"
	@echo "  make install    Install dependencies"
	@echo "  make build      Build containers"
	@echo "  make up         Start containers"
	@echo "  make down       Stop containers"
	@echo "  make run        Run dispatcher"
	@echo "  make test       Run full test"
	@echo "  make logs       Show logs"
	@echo "  make ps         Show container status"
	@echo "  make health     Check system health"
	@echo "  make load-test  Run load test"
	@echo "  make clean      Clean up"

setup:
	./setup.sh

install:
	pip install -r requirements.txt

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

run:
	python dispatch.py

test: install build up
	@sleep 3
	python dispatch.py
	$(MAKE) down

logs:
	docker-compose logs

ps:
	docker-compose ps

health:
	@echo "Checking system health..."
	@rabbitmqctl status > /dev/null 2>&1 && echo "RabbitMQ: OK" || echo "RabbitMQ: ERROR"
	@docker-compose ps --format table

load-test:
	python -c "from celery_app import task_a, task_b; import time; start=time.time(); results=[task_a.delay().get() for _ in range(5)] + [task_b.delay().get() for _ in range(5)]; print(f'Completed {len(results)} tasks in {time.time()-start:.2f}s')"

clean:
	docker-compose down -v
	docker system prune -f
	rm -f dispatch_results_*.json
