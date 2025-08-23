import torch
from model_loader import pipe, tokenizer


def handler(job):
    print("Worker Start")

    job_input = job.get("input", {})
    if not job_input.get("prompt"):
        return {
            "error": "Input is missing the 'prompt' key. Please include a prompt.")
        }

    if pipe is None or tokenizer is None:
        print("Pipeline/Tokenizer not loaded. Exiting.")
        return {"error": "Model pipeline not loaded."}

    # Read generation params with sane defaults
    prompt = job_input["prompt"]
    do_sample = bool(job_input.get("do_sample", True))
    max_new_tokens = int(job_input.get("max_new_tokens", 100))
    temperature = float(job_input.get("temperature", 0.7))
    top_k = int(job_input.get("top_k", 50))
    top_p = float(job_input.get("top_p", 0.95))
    num_return_sequences = int(job_input.get("num_return_sequences", 1))
    repetition_penalty = float(job_input.get("repetition_penalty", 1.0))
    seed = job_input.get("seed")

    generator = None
    if seed is not None:
        try:
            generator = torch.Generator(device="cuda").manual_seed(int(seed))
        except Exception:
            generator = None

    print(f"Received prompt: {prompt}")
    print("Prompt started processing")

    sequences = pipe(
        prompt,
        do_sample=do_sample,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        num_return_sequences=num_return_sequences,
        repetition_penalty=repetition_penalty,
        return_full_text=False,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        generator=generator,
    )

    # Use the first sequence
    text = sequences[0]["generated_text"] if sequences else ""

    # Token counts for basic observability
    try:
        tokens_generated = len(tokenizer.encode(text))
        prompt_tokens = len(tokenizer.encode(prompt))
    except Exception:
        tokens_generated = None
        prompt_tokens = None

    print("Prompt finished processing", text)

    return {
        "text": text,
        "meta": {
            "prompt": prompt,
            "do_sample": do_sample,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "num_return_sequences": num_return_sequences,
            "repetition_penalty": repetition_penalty,
            "seed": seed,
            "prompt_tokens": prompt_tokens,
            "tokens_generated": tokens_generated,
        },
    }
