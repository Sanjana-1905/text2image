import os
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import Dict
from threading import Lock

from app.generator_api import generate_image_bytes
from app.transcriber import transcribe

app = FastAPI()
# In-memory progress store
progress_store: Dict[str, int] = {}
progress_lock = Lock()

# Allow localhost dev server (http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists and mount it
os.makedirs("app/static/images", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.post("/transcribe")
async def endpoint_transcribe(audio: UploadFile = File(...)):
    tmp = f"tmp_{uuid.uuid4().hex}.webm"
    data = await audio.read()
    with open(tmp, "wb") as f:
        f.write(data)
    
    try:
        text = transcribe(tmp)
    except Exception as e:
        print(f"[ERROR] Transcription failed: {str(e)}")
        return JSONResponse({"error": "Transcription failed"}, status_code=500)
    finally:
        try:
            os.remove(tmp)
        except Exception:
            pass

    return {"text": text}

from app.generator_api import generate_image_bytes

@app.post("/generate")
async def endpoint_generate(prompt: str = Form(...), progress_key: str = Form(None)):
    try:
        def report(pct: int):
            if not progress_key:
                return
            with progress_lock:
                progress_store[progress_key] = pct

        img_bytes = generate_image_bytes(prompt, progress_callback=report)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    fname = f"{uuid.uuid4().hex}.png"
    path = os.path.join("app/static/images", fname)
    with open(path, "wb") as f:
        f.write(img_bytes)

    return {"url": f"/static/images/{fname}"}

@app.get("/progress/{key}")
def get_progress(key: str):
    with progress_lock:
        pct = progress_store.get(key, 0)
        if pct >= 100:
            # clean up finished keys
            try:
                del progress_store[key]
            except Exception:
                pass
        return {"progress": pct}