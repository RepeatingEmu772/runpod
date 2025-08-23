import base64
import io
from typing import Optional

import torch
from PIL import Image

from model_loader import pipe_t2i, pipe_i2i


def _img_to_b64(img: Image.Image, fmt: str = "PNG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def _b64_to_img(data: str) -> Image.Image:
    raw = base64.b64decode(data)
    return Image.open(io.BytesIO(raw)).convert("RGB")


def handler(job):
    print("Image Worker Start")

    job_input = job.get("input", {})

    prompt = job_input.get("prompt")
    if not prompt:
        return {"error": "Input must include 'prompt'."}

    if pipe_t2i is None:
        return {"error": "Model pipeline not loaded."}

    negative_prompt = job_input.get("negative_prompt", "")
    width = int(job_input.get("width", 1024))
    height = int(job_input.get("height", 1024))
    steps = int(job_input.get("num_inference_steps", 12))  
    guidance = float(job_input.get("guidance_scale", 3.5))
    seed = job_input.get("seed")

    generator: Optional[torch.Generator] = None
    if seed is not None:
        try:
            generator = torch.Generator(device="cuda").manual_seed(int(seed))
        except Exception:
            generator = None

    init_b64 = job_input.get("init_image_b64")
    strength = float(job_input.get("strength", 0.5))  # how much to deviate from init image

    if init_b64:
        if pipe_i2i is None:
            return {"error": "This build does not include FLUX image-to-image support. Omit 'init_image_b64' or update diffusers."}
        init_img = _b64_to_img(init_b64).resize((width, height), Image.LANCZOS)
        out = pipe_i2i(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=init_img,
            strength=strength,
            num_inference_steps=steps,
            guidance_scale=guidance,
            generator=generator,
        )
    else:
        out = pipe_t2i(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=steps,
            guidance_scale=guidance,
            width=width,
            height=height,
            generator=generator,
        )

    img = out.images[0]
    img_b64 = _img_to_b64(img, "PNG")

    return {
        "image_b64": img_b64,
        "meta": {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "guidance": guidance,
            "seed": seed,
            "mode": "img2img" if init_b64 and pipe_i2i else "t2i",
        },
    }
