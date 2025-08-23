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
Uses Mistral-7B model for text generation with 4-bit quantization.

### Image Processing (`endpoints/image/`)
Template for image processing tasks.

## Development

### Setup

1. Create a virtual environment and install dependencies:
```bash
make
```

2. Set your Hugging Face token (for text endpoint):
```bash
export HF_TOKEN=your_hugging_face_token
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

### Deploy to RunPod

1. Push your image to a container registry:
```bash
docker tag runpod-text:latest your-registry/runpod-text:latest
docker push your-registry/runpod-text:latest
```

2. Create a new endpoint on RunPod using your image URL.

## Adding New Endpoints

1. Create a new directory under `endpoints/`
2. Follow the same structure as existing endpoints:
   - `src/main.py` - Entry point
   - `src/handler.py` - Request handler
   - `src/model_loader.py` - Model loading logic
   - `Dockerfile` - Container configuration
3. Update the Makefile with new targets
4. Add the new endpoint to the main Dockerfile if needed

## Testing

Run tests across all endpoints:
```bash
make test
```

## Code Quality

Lint all endpoint code:
```bash
make lint
```