from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uuid
import os

from app.tts_service import pdf_to_audio, hello

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    "https://resonate-frontend.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

hello()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
os.makedirs(TEMP_DIR, exist_ok=True)


def cleanup_files(*paths):
    for path in paths:
        try:
            if path.startswith(TEMP_DIR) and os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Cleanup failed for {path}: {e}")


@app.post("/convert")
async def convert_pdf(
    background_tasks: BackgroundTasks,
    pdf: UploadFile = File(...)
):
    temp_pdf = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pdf")
    mp3_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")

    # Save PDF
    with open(temp_pdf, "wb") as f:
        f.write(await pdf.read())

    # Convert
    pdf_to_audio(temp_pdf, mp3_path)

    # ✅ Cleanup AFTER response is sent
    background_tasks.add_task(cleanup_files, temp_pdf, mp3_path)

    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename="result.mp3",
        background=background_tasks
    )
