import sys
import runpod
from handler import handler
from model_loader import load_models

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Incorrect usage\nSample usage: python main.py <env>")
        sys.exit(1)

    env = sys.argv[1]
    print(f"env: {env}")
    load_models(env)

    runpod.serverless.start({"handler": handler})
