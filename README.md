# RunPod Endpoints

A collection of serverless endpoints for RunPod, organized by functionality.

## Project Structure

```
runpod/
├── Dockerfile                    # Multi-stage build for different endpoints
├── Makefile                      # Build and run commands
├── builder/
│   └── requirements.txt          # Python dependencies
├── endpoints/                    # Endpoint implementations
│   ├── text/                    # Text generation endpoint
│   │   ├── Dockerfile           # Text-specific Dockerfile
│   │   └── src/
│   │       ├── main.py          # Entry point
│   │       ├── handler.py       # Request handler
│   │       └── model_loader.py  # Model loading logic
│   └── image/                   # Image processing endpoint
│       ├── Dockerfile           # Image-specific Dockerfile
│       └── src/
│           ├── main.py          # Entry point
│           ├── handler.py       # Request handler
│           └── model_loader.py  # Model loading logic
└── test_input.json              # Example input for testing
```

## Available Endpoints

### Text Generation (`endpoints/text/`)
Mistral-7B 4-bit quantization

### Image Processing (`endpoints/image/`)
Flux.1-dev

## Development

### Setup

1. Create a virtual environment and install dependencies:
```bash
make
```

### Running Endpoints Locally

**Text endpoint:**
```bash
make run-text-local
```

**Image endpoint:**
```bash
make run-image-local
```

### Running in Staging Mode

**Text endpoint:**
```bash
make run-text-stg
```

**Image endpoint:**
```bash
make run-image-stg
```

## Building and Deploying

### Build Individual Endpoints

**Text endpoint:**
```bash
make build-text
```

**Image endpoint:**
```bash
make build-image
```

**Build all endpoints:**
```bash
make build-all
```

### Build Using Multi-stage Dockerfile

**Text endpoint:**
```bash
docker build --build-arg ENDPOINT=text -t runpod-text:latest .
```

**Image endpoint:**
```bash
docker build --build-arg ENDPOINT=image -t runpod-image:latest .
```