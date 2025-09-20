.PHONY: help install build up down run test logs ps clean venv monitor scale status

help:
	@echo "Usage:"
	@echo "  make install    Install dependencies in virtual environment"
	@echo "  make build      Build containers"
	@echo "  make up         Start containers (includes RabbitMQ)"
	@echo "  make down       Stop containers"
	@echo "  make run        Run dispatcher"
	@echo "  make test       Run full test"
	@echo "  make logs       Show logs"
	@echo "  make ps         Show container status"
	@echo "  make monitor    Show task monitoring logs"
	@echo "  make scale      Scale workers (usage: make scale QUEUE=worker-a COUNT=3)"
	@echo "  make scale-all  Scale all workers (usage: make scale-all COUNT=3)"
	@echo "  make status     Show scaling status"
	@echo "  make load-test  Run load test (usage: make load-test TASKS=20)"
	@echo "  make clean      Clean up"

venv:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip

install: venv
	./venv/bin/pip install -r requirements.txt

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

run:
	source venv/bin/activate && python dispatch.py

test: install build up
	@sleep 2
	source venv/bin/activate && python dispatch.py
	$(MAKE) down

logs:
	docker-compose logs

ps:
	docker-compose ps

monitor:
	docker-compose logs -f --tail=50

scale:
	@if [ -z "$(QUEUE)" ] || [ -z "$(COUNT)" ]; then \
		echo "Usage: make scale QUEUE=worker-a COUNT=3"; \
		exit 1; \
	fi
	source venv/bin/activate && python scale.py scale --queue $(QUEUE) --count $(COUNT)

scale-all:
	@if [ -z "$(COUNT)" ]; then \
		echo "Usage: make scale-all COUNT=3"; \
		exit 1; \
	fi
	source venv/bin/activate && python scale.py scale-all --all-count $(COUNT)

status:
	source venv/bin/activate && python scale.py status

load-test:
	@TASKS=$${TASKS:-20}; \
	echo "Running load test with $$TASKS tasks of each type..."; \
	source venv/bin/activate && python load_test.py --tasks $$TASKS

clean:
	docker-compose down -v
	docker system prune -f
	rm -rf venv
