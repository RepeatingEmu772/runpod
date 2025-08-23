import torch
from transformers import pipeline
from model_loader import model, tokenizer

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
        return "not processed"

    pipe = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
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


