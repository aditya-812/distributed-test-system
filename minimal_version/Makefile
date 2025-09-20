.PHONY: help install build up down run test logs ps clean venv

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

clean:
	docker-compose down -v
	docker system prune -f
	rm -rf venv
