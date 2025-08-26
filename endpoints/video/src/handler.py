import base64
import io
import os
import tempfile
from typing import Optional

import torch
from moviepy.editor import ImageSequenceClip

from model_loader import pipe_video


def _bytes_to_b64(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")


def _frames_to_mp4_bytes(frames, fps: int):
    # frames are expected to be PIL.Image or numpy arrays
    tmp_dir = tempfile.mkdtemp(prefix="runpod_video_")
    out_path = os.path.join(tmp_dir, "out.mp4")
    clip = ImageSequenceClip([f for f in frames], fps=fps)
    # moviepy writes to a file
    clip.write_videofile(out_path, codec="libx264", fps=fps, verbose=False, logger=None)
    with open(out_path, "rb") as fh:
        data = fh.read()

    # cleanup
    try:
        os.remove(out_path)
        os.rmdir(tmp_dir)
    except Exception:
        pass

    return data


def handler(job):
    print("Video Worker Start")

    job_input = job.get("input", {})

    prompt = job_input.get("prompt")
    if not prompt:
        return {"error": "Input must include 'prompt'."}

    if pipe_video is None:
        return {"error": "Video pipeline not loaded in this build."}

    width = int(job_input.get("width", 640))
    height = int(job_input.get("height", 360))
    fps = int(job_input.get("fps", 15))
    duration = float(job_input.get("duration", 3.0))
    steps = int(job_input.get("num_inference_steps", 12))
    guidance = float(job_input.get("guidance_scale", 3.5))
    seed = job_input.get("seed")

    generator: Optional[torch.Generator] = None
    if seed is not None:
        try:
            generator = torch.Generator(device="cuda").manual_seed(int(seed))
        except Exception:
            generator = None

    # The exact call shape depends on the pipeline implementation. We'll try a
    # few reasonable parameter names and handle two common return shapes:
    #  - an object with `.videos[0]` or `.video` as raw bytes
    #  - an object with `.frames` or `.images` as a list of frames (PIL/numpy)
    try:
        out = pipe_video(
            prompt=prompt,
            height=height,
            width=width,
            fps=fps,
            duration=duration,
            num_inference_steps=steps,
            guidance_scale=guidance,
            generator=generator,
        )
    except TypeError:
        # Fallback to a more generic call without type-specific args
        out = pipe_video(prompt=prompt)

    # Try to extract video bytes
    video_bytes = None
    frames = None

    if hasattr(out, "videos"):
        try:
            video_bytes = out.videos[0]
        except Exception:
            video_bytes = None

    if video_bytes is None and hasattr(out, "video"):
        try:
            video_bytes = out.video
        except Exception:
            video_bytes = None

    if video_bytes is None and hasattr(out, "frames"):
        frames = out.frames

    if video_bytes is None and hasattr(out, "images"):
        frames = out.images

    if video_bytes is None and frames:
        # Convert frames -> mp4 bytes
        mp4 = _frames_to_mp4_bytes(frames, fps)
        video_bytes = mp4

    if video_bytes is None:
        return {"error": "Pipeline returned an unexpected format; cannot extract video."}

    video_b64 = _bytes_to_b64(video_bytes)

    return {
        "video_b64": video_b64,
        "meta": {
            "prompt": prompt,
            "width": width,
            "height": height,
            "fps": fps,
            "duration": duration,
            "steps": steps,
            "guidance": guidance,
            "seed": seed,
        },
    }
