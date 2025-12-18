from gtts import gTTS
from PyPDF2 import PdfReader

def pdf_to_audio(input_pdf_path, output_audio_path):
    reader = PdfReader(input_pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    tts = gTTS(text)
    tts.save(output_audio_path)

    return output_audio_path

def hello():
    print("hello function called")
