import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline

# Globals populated by load_models()
model = None
tokenizer = None
pipe = None

def fetch_token():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN environment variable not set.")
    return token

def load_models(env):
    """
    Loads the Mistral model/tokenizer and constructs a reusable text-generation pipeline.
    On 'local', we intentionally avoid loading to speed local dev without GPU.
    """
    global model, tokenizer, pipe

    if env == 'local':
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

    # Load tokenizer and model
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

    # Build the generation pipeline ONCE and reuse in the handler
    # Note: For quantized models, dtype here is largely ignored for weights but fine for buffers
    global_pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    # Assign to the module-level global
    pipe = global_pipe