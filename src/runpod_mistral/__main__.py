#!/usr/bin/env python
"""Main entry point for RunPod serverless worker."""

import sys
import runpod
from runpod_mistral.handler import handler, load_models

def main():
    """Main function to start the RunPod serverless worker."""
    if len(sys.argv) < 2:
        print("Incorrect usage\nSample usage: python -m runpod_mistral <env>")
        sys.exit(1)
    
    env = sys.argv[1]
    print(f"Environment: {env}")
    load_models(env) 

    runpod.serverless.start({'handler': handler})

if __name__ == '__main__':
    main()
