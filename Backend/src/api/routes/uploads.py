from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from datetime import datetime
import shutil

router = APIRouter()

# --------------------------------------------------
# ABSOLUTE PATH TO Backend/data/raw
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_FOLDER = BASE_DIR / "data" / "raw"

RAW_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# --------------------------------------------------
# UPLOAD EXCEL
# --------------------------------------------------

@router.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...)
):

    if not file.filename.endswith((".xlsx", ".xls")):
        return {
            "success": False,
            "message": "Only Excel files are allowed"
        }

    file_path = RAW_FOLDER / file.filename

    print(f"Saving file to: {file_path}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "success": True,
        "message": f"{file.filename} uploaded successfully"
    }


# --------------------------------------------------
# GET ALL UPLOADED FILES
# --------------------------------------------------

@router.get("/uploads")
def get_uploaded_files():

    files = []

    for file in RAW_FOLDER.glob("*"):

        if file.is_file():

            stat = file.stat()

            files.append(
                {
                    "file_name": file.name,

                    "size_mb": round(
                        stat.st_size / (1024 * 1024),
                        2
                    ),

                    "upload_date": datetime
                    .fromtimestamp(
                        stat.st_mtime
                    )
                    .strftime("%d %b %Y"),

                    # used only for sorting
                    "timestamp": stat.st_mtime,

                    "status": "Success"
                }
            )

    # --------------------------------------------------
    # SORT BY ACTUAL FILE MODIFIED TIME
    # NEWEST FILES FIRST
    # --------------------------------------------------

    files.sort(
        key=lambda item: item["timestamp"],
        reverse=True
    )

    # --------------------------------------------------
    # REMOVE INTERNAL FIELD
    # --------------------------------------------------

    for item in files:
        item.pop("timestamp")

    return files