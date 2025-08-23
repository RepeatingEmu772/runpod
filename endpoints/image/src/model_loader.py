import os

model = None

def load_models(env):
    global model

    if env == 'local':
        model = None
        return 

    # Placeholder for image model loading
    print(f"Loading image models for environment: {env}")
