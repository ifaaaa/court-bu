from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import shutil
import os
from anonymizer import anonymize_docx

app = FastAPI()

# Static файлуудыг зөвхөн "static" хавтсаас авч байгаагаа зөв тохируулна
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    input_path = f"temp/{file.filename}"
    output_path = f"temp/нууцалсан_{file.filename}"

    os.makedirs("temp", exist_ok=True)
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    anonymize_docx(input_path, output_path)

    return FileResponse(output_path, filename=f"нууцалсан_{file.filename}")
