import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generator_api import generate_image_bytes

prompt = "A white cat sitting on a sofa in a cosy living room, highly detailed"

try:
    img_bytes = generate_image_bytes(prompt)
    with open("test_output.png", "wb") as f:
        f.write(img_bytes)
    print("Image generated successfully!")
except Exception as e:
    print(f"Failed: {str(e)}")