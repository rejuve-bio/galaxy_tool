# Variables
HOST = 100.67.47.42
PROD_PORT = 9094
DEV_PORT = 9095
GALAXY_ROOT = ../galaxy 

activate-env:
		. .venv/bin/activate

start-planemo-prod:
	@echo "Starting Planemo server on host $(HOST) and port $(PROD_PORT)"
	make activate-env
	planemo s --host=$(HOST) --port=$(PROD_PORT) --galaxy_root=$(GALAXY_ROOT)

start-planemo-dev:
	@echo "Starting Planemo server on host $(HOST) and port $(DEV_PORT)"
	make activate-env
	. .venv/bin/activate
	planemo s --host=$(HOST) --port=$(DEV_PORT) --galaxy_root=$(GALAXY_ROOT)
