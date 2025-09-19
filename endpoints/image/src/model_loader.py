import os
import torch
from diffusers import FluxPipeline

try:
    from diffusers import FluxImg2ImgPipeline  
    _HAS_I2I = True
except Exception:
    FluxImg2ImgPipeline = None  
    _HAS_I2I = False

pipe_t2i = None
pipe_i2i = None


def _fetch_token() -> str:
    token = os.getenv("HF_TOKEN")
    if not token:
        raise ValueError("HF_TOKEN environment variable not set.")
    return token


def load_models(env: str):
    """
    Load FLUX.1-dev pipelines (text->image, optional image->image) once at cold start.
    """
    global pipe_t2i, pipe_i2i

    if env == "local":
        pipe_t2i = None
        pipe_i2i = None
        return

    token = _fetch_token()
    model_id = "black-forest-labs/FLUX.1-dev"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    pipe_t2i = FluxPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        use_safetensors=True,
        token=token,
    )
    pipe_t2i = pipe_t2i.to("cuda" if torch.cuda.is_available() else "cpu")

    try:
        pipe_t2i.enable_attention_slicing()
    except Exception:
        pass
    if hasattr(pipe_t2i, "vae"):
        try:
            pipe_t2i.vae.enable_slicing()
            pipe_t2i.vae.enable_tiling()
        except Exception:
            pass

    if _HAS_I2I:
        try:
            pipe_i2i = FluxImg2ImgPipeline.from_pretrained(
                model_id,
                torch_dtype=dtype,
                use_safetensors=True,
                token=token,
            )
            pipe_i2i = pipe_i2i.to("cuda" if torch.cuda.is_available() else "cpu")
            try:
                pipe_i2i.enable_attention_slicing()
            except Exception:
                pass
            if hasattr(pipe_i2i, "vae"):
                try:
                    pipe_i2i.vae.enable_slicing()
                    pipe_i2i.vae.enable_tiling()
                except Exception:
                    pass
        except Exception:
            pipe_i2i = None
    else:
        pipe_i2i = None
