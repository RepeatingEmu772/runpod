import sys
import runpod
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model = None 
tokenizer = None

def load_models():
    # Load model and tokenizer outside the handler
    model_name = "mistralai/Mistral-7B-v0.1"
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        quantization_config=bnb_config,
        torch_dtype=torch.bfloat16,
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
    
    if model is not None print(f"found model")
    if tokenizer is not None print(f"found tokenizer")

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
    print("Prompt finished processing "sequences[0]['generated_text'])
    
    return sequences[0]['generated_text']

if __name__ == '__main__':
    env = "stg" if (len(sys.argv) < 1) else "local"
    load_models() if env != 'local' else print("local testing. skipping loading models...") 

    runpod.serverless.start({'handler': handler })
