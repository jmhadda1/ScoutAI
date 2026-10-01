from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from analyzer import analyze_listing

app = FastAPI(title="Scout AI")

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {

        "application": "Scout AI",

        "status": "running"

    }


@app.post("/analyze")
async def analyze(

    file: UploadFile = File(...)

):

    save_path = os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )

    with open(save_path, "wb") as buffer:

        shutil.copyfileobj(

            file.file,

            buffer

        )

    result = analyze_listing(

        save_path

    )

    return result