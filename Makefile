# Variables
PYTHON := python3
PIP := pip3
VENV := venv
ENDPOINTS_DIR := endpoints
TEXT_ENDPOINT := $(ENDPOINTS_DIR)/text
IMAGE_ENDPOINT := $(ENDPOINTS_DIR)/image
TEXT_REQ := $(TEXT_ENDPOINT)/builder/requirements.txt
IMAGE_REQ := $(IMAGE_ENDPOINT)/src/builder/requirements.txt

# Create virtual environment for text endpoint
$(VENV)/bin/activate: $(TEXT_REQ)
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate; $(PIP) install --upgrade pip
	. $(VENV)/bin/activate; $(PIP) install -r $(TEXT_REQ)
	. $(VENV)/bin/activate; $(PIP) install -r $(IMAGE_REQ) 

# Run the text endpoint locally
run-text-local: $(VENV)/bin/activate
	. $(VENV)/bin/activate; cd $(TEXT_ENDPOINT) && PYTHONPATH=src $(PYTHON) src/main.py local

# Run the text endpoint in staging mode
run-text-stg: $(VENV)/bin/activate
	. $(VENV)/bin/activate; cd $(TEXT_ENDPOINT) && PYTHONPATH=src $(PYTHON) src/main.py stg

# Run the image endpoint locally
run-image-local: $(VENV)/bin/activate
	. $(VENV)/bin/activate; cd $(IMAGE_ENDPOINT) && PYTHONPATH=src $(PYTHON) src/main.py local

# Run the image endpoint in staging mode
run-image-stg: $(VENV)/bin/activate
	. $(VENV)/bin/activate; cd $(IMAGE_ENDPOINT) && PYTHONPATH=src $(PYTHON) src/main.py stg

# Build Docker image for text endpoint
build-text:
	docker build -t runpod-text:latest -f $(TEXT_ENDPOINT)/Dockerfile .

# Build Docker image for image endpoint
build-image:
	docker build -t runpod-image:latest -f $(IMAGE_ENDPOINT)/Dockerfile .

# Build all endpoints
build-all: build-text build-image

# Run tests
test: $(VENV)/bin/activate
	. $(VENV)/bin/activate; pytest -v

# Lint with flake8
lint: $(VENV)/bin/activate
	. $(VENV)/bin/activate; flake8 $(ENDPOINTS_DIR)

# Clean up
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache *.pyc
	find $(ENDPOINTS_DIR) -name "__pycache__" -type d -exec rm -rf {} +
	find $(ENDPOINTS_DIR) -name "*.pyc" -delete

.PHONY: run-text-local run-text-stg run-image-local run-image-stg build-text build-image build-all test lint clean