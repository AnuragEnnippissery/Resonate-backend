from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uuid
import os

from app.tts_service import pdf_to_audio, hello

app = FastAPI()

# ✅ CORS MUST be here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
        if path.startswith(TEMP_DIR) and os.path.exists(path):
            os.remove(path)

'''@app.post("/convert")
async def convert_pdf(
    background_tasks: BackgroundTasks,
    pdf: UploadFile = File(...)
):
    temp_pdf = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pdf")
    with open(temp_pdf, "wb") as f:
        f.write(await pdf.read())

    mp3_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")
    pdf_to_audio(temp_pdf, mp3_path)

    background_tasks.add_task(cleanup_files, temp_pdf, mp3_path)

    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename="result.mp3",
        background=background_tasks
    )'''
@app.post("/convert")
async def convert_pdf(pdf: UploadFile = File(...)):
        temp_pdf = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.pdf")
        with open(temp_pdf, "wb") as f:
            f.write(await pdf.read())

        mp3_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.mp3")
        pdf_to_audio(temp_pdf, mp3_path)

        return FileResponse(
            mp3_path,
            media_type="audio/mpeg",
            filename="result.mp3"
    )

