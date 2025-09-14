# generator_api.py
import torch
from diffusers import StableDiffusionPipeline
from io import BytesIO

# -----------------------------
# Configuration
# -----------------------------
MODEL_ID = "runwayml/stable-diffusion-v1-5"  # You can change to any diffusers-supported model
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32

# -----------------------------
# Load the Stable Diffusion Pipeline
# -----------------------------
print(f"Loading model '{MODEL_ID}' on device '{DEVICE}'...")
pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=TORCH_DTYPE)
pipe = pipe.to(DEVICE)
print("Model loaded successfully!")

# -----------------------------
# Image generation function
# -----------------------------
def generate_image_bytes(prompt: str, width: int = 512, height: int = 512) -> bytes:
    """
    Generate an image from a text prompt using Stable Diffusion.
    Returns image bytes in PNG format.
    
    Args:
        prompt (str): Text prompt for the image.
        width (int): Image width in pixels.
        height (int): Image height in pixels.

    Returns:
        bytes: PNG image bytes.
    """
    # Generate image
    image = pipe(prompt, height=height, width=width).images[0]

    # Convert image to bytes
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()