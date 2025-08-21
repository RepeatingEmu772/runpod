# RunPod Mistral Worker

A serverless worker for running the Mistral-7B language model on RunPod.

## Project Structure

The project has been organized using a modern Python package structure with `pyproject.toml`:

```
runpod/
├── pyproject.toml          # Project metadata and dependencies
├── Dockerfile              # Container configuration
├── Makefile                # Build and run commands
├── src/                    # Source code
│   └── runpod_mistral/     # Package directory
│       ├── __init__.py     # Package initialization
│       ├── __main__.py     # Entry point
│       └── handler.py      # RunPod handler implementation
└── test_input.json         # Example input for testing
```

## Development

### Setup

1. Create a virtual environment and install dependencies:

```bash
make
```

2. Set your Hugging Face token as an environment variable:

```bash
export HF_TOKEN=your_hugging_face_token
```

### Running Locally

```bash
make run-local
```

### Running in Staging Mode

```bash
make run-stg
```

### Code Formatting

```bash
make format
```

### Running Tests

```bash
make test
```

## Building and Deploying

Build the Docker image:

```bash
docker build -t runpod-mistral:latest .
```

Push to your container registry:

```bash
docker tag runpod-mistral:latest your-registry/runpod-mistral:latest
docker push your-registry/runpod-mistral:latest
```

## License

MIT
