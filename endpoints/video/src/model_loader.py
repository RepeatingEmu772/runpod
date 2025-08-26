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
    """
    Load a WAN-2.2 video pipeline. On 'local' we skip loading so local dev doesn't
    need GPU or large downloads. If the environment lacks the required classes
    the module-level `pipe_video` will remain None and handlers will return an
    informative error.
    """
    global pipe_video

    if env == "local":
        pipe_video = None
        return

    try:
        token = _fetch_token()
    except Exception:
        pipe_video = None
        return

    # Replace this with the real model id for WAN 2.2 if different
    MODEL_ID = "wan/wan2.2"

    # Choose dtype based on CUDA availability
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    try:
        # Try to load a generic video-capable pipeline from diffusers.
        # Note: concrete class names and APIs differ between implementations;
        # this is a best-effort loader that will silently degrade to None if
        # the exact class isn't present in the environment.
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
        # If we cannot import or construct a pipeline, leave pipe_video as None.
        pipe_video = None
