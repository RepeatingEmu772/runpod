import sys
import os
import runpod
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def fetch_token():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN environment variable not set.")
    return token

def load_models(env):
    # Load model and tokenizer outside the handler
    global model, tokenizer

    if env == 'local':
        model = None
        tokenizer = None
        return 

    model_name = "mistralai/Mistral-7B-v0.1"
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=fetch_token()
        )

    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        quantization_config=bnb_config,
        torch_dtype=torch.bfloat16,
        token=fetch_token()
        )
    
    # # Move model to GPU if available
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # model.to(device)

def handler(job):
    print("Worker Start")
    
    job_input = job["input"]

    if not job_input.get("prompt", False):
        return {
            "error": "Input is missing the 'prompt' key. Please include a prompt."
        }

    prompt = job_input.get('prompt')  
    seconds = job_input.get('seconds', 0)  

    print(f"Received prompt: {prompt}")
    
    if model is None or tokenizer is None:
        print("Model/Tokenizer not found. Skipping exiting..")
        return "not proccessed"

    pipe = pipeline(
        "text-generation", 
        model=model, 
        tokenizer = tokenizer, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
        )

    print("Prompt started processing")

    sequences = pipe(
        prompt,
        do_sample=True,
        max_new_tokens=100, 
        temperature=0.7, 
        top_k=50, 
        top_p=0.95,
        num_return_sequences=1,
        )
    print("Prompt finished processing ", sequences[0]['generated_text'])
    
    return sequences[0]['generated_text']

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Incorrect usage\nSample usage: python handler.py <env>")
    
    env = sys.argv[1]
    print(f"env: {env}")
    load_models(env) 

    runpod.serverless.start({'handler': handler })
