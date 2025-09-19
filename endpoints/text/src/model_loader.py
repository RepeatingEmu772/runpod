import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

model = None
tokenizer = None
pipe = None

def fetch_token():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN environment variable not set.")
    return token

def load_models(env):
    global model, tokenizer, pipe

    if env == 'local':
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

            small_model_name = "distilgpt2"
            tokenizer = AutoTokenizer.from_pretrained(small_model_name)
            model = AutoModelForCausalLM.from_pretrained(small_model_name, device_map="cpu")
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device_map="cpu",
            )
            return
        except Exception:
            model = None
            tokenizer = None
            pipe = None
            return

    token = fetch_token()
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"

    # 4-bit quantization for efficient VRAM use on serverless GPUs
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
        torch_dtype=torch.bfloat16,  # dtype for non-quant buffers
        token=token
    )

    global_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    pipe = global_pipe