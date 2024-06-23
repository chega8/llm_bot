.PHONY: init
init:
	poetry run python src/scripts/init_db.py

.PHONY: run-server
run-server:
	poetry run python src/grpc_llm/llm_server.py

.PHONY: run-app
run-app:
	poetry run python src/app.py
