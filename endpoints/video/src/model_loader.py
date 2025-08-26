import os
import torch
import tempfile

pipe_video = None

def _fetch_token():
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN environment variable not set.")
    return token

def load_models(env: str):
    global pipe_video

    if env == "local":
        pipe_video = None
        return

    try:
        token = _fetch_token()
    except Exception:
        pipe_video = None
        return

    MODEL_ID = "Wan-AI/Wan2.2-TI2V-5B"

    # Choose dtype based on CUDA availability
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    try:
        from diffusers import VideoPipeline

        pipe = VideoPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
            use_safetensors=True,
            token=token,
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)

        try:
            pipe.enable_attention_slicing()
        except Exception:
            pass

        pipe_video = pipe
    except Exception:
        pipe_video = None
