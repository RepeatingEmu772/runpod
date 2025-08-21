# Variables
PYTHON := python3
PIP := pip3
VENV := venv
SRC := src

# Create virtual environment
$(VENV)/bin/activate: pyproject.toml
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate; $(PIP) install --upgrade pip
	. $(VENV)/bin/activate; $(PIP) install -e ".[dev]"

# Run the app
run-local: $(VENV)/bin/activate
	. $(VENV)/bin/activate; $(PYTHON) -m runpod_mistral local

run-stg: $(VENV)/bin/activate
	. $(VENV)/bin/activate; $(PYTHON) -m runpod_mistral stg

# Format code
format: $(VENV)/bin/activate
	. $(VENV)/bin/activate; isort $(SRC)
	. $(VENV)/bin/activate; black $(SRC)

# Run tests (pytest)
test: $(VENV)/bin/activate
	. $(VENV)/bin/activate; pytest -v

# Clean up
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache *.pyc

.PHONY: run-local run-stg format test clean