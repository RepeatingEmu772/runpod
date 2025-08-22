import sys
import os
import runpod
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

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

    token = fetch_token()
    model_name = "mistralai/Mistral-7B-v0.1"
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        )
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=token
        )

    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        quantization_config=bnb_config,
        torch_dtype=torch.bfloat16,
        token=token
        )