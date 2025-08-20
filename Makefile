# Variables
PYTHON := python3
PIP := pip3
VENV := venv
SRC := src
REQ := builder/requirements.txt

# Create virtual environment
$(VENV)/bin/activate: $(REQ)
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate; $(PIP) install --upgrade pip
	. $(VENV)/bin/activate; $(PIP) install -r $(REQ) 

# Run the app
run-local: $(VENV)/bin/activate
	. $(VENV)/bin/activate; $(PYTHON) $(SRC)/handler.py local

run-stg: $(VENV)/bin/activate
	. $(VENV)/bin/activate; $(PYTHON) $(SRC)/handler.py stg

# Run tests (pytest)
test: $(VENV)/bin/activate
	. $(VENV)/bin/activate; pytest -v

# Lint with flake8
lint: $(VENV)/bin/activate
	. $(VENV)/bin/activate; flake8 $(SRC)

# Clean up
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache *.pyc

.PHONY: run test lint clean