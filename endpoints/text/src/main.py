from 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect usage\nSample usage: python handler.py <env>")
    
    env = sys.argv[1]
    print(f"env: {env}")
    load_models(env) 

    runpod.serverless.start({'handler': handler })