'''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Sample database
userlist = {
    "user1": {"fname": "anu", "roll": 21},
    "user2": {"fname": "sonu", "roll": 22}
}

# Request model for adding/updating user
class User(BaseModel):
    fname: str
    roll: int


# HOME ROUTE
@app.get("/")
def root():
    return {"message": "FastAPI working!"}


# GET — Fetch a specific user
@app.get("/user/{username}")
def get_user(username: str):
    if username not in userlist:
        raise HTTPException(status_code=404, detail="User not found")
    return userlist[username]


# POST — Add a new user
@app.post("/user")
def add_user(username: str, user: User):
    if username in userlist:
        raise HTTPException(status_code=400, detail="User already exists")

    userlist[username] = user.model_dump()  # store data
    return {"message": "User added successfully", "user": userlist[username]}


# PUT — Update existing user
@app.put("/user/{username}")
def update_user(username: str, user: User):
    if username not in userlist:
        raise HTTPException(status_code=404, detail="User not found")

    userlist[username] = user.model_dump()
    return {"message": "User updated successfully", "user": userlist[username]}'''

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uuid
import os

from app.tts_service import pdf_to_audio
from app.tts_service import hello

app = FastAPI()
hello()

@app.post("/convert")
async def convert_pdf(pdf: UploadFile = File(...)):
    # Save uploaded PDF temporarily
    temp_pdf = f"{uuid.uuid4()}.pdf"
    with open(temp_pdf, "wb") as f:
        f.write(await pdf.read())

    # Output audio filename
    output_mp3 = f"{uuid.uuid4()}.mp3"

    # Convert PDF → Audio
    mp3_path = pdf_to_audio(temp_pdf, output_mp3)

    # Return the actual audio file back
    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename="result.mp3"
    )

