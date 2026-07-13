from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import subprocess
import traceback

from api.services.uploads_service import (
    get_report_type,
    append_incident_master,
    append_request_master
)

router = APIRouter()

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_FOLDER = BASE_DIR / "data" / "raw"
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

PIPELINE_FOLDER = BASE_DIR / "src" / "pipeline"

AMS_SCRIPT = PIPELINE_FOLDER / "step2_ticket_master.py"
AGG_SCRIPT = PIPELINE_FOLDER / "step1_aggregation.py"
ASSET_SCRIPT = PIPELINE_FOLDER / "Asset_count.py"
SOFTWARE_SCRIPT = PIPELINE_FOLDER / "software_requisition.py"

# =====================================================
# UPLOAD
# =====================================================

@router.post("/upload-excel")
async def upload_excel(

    upload_type: str = Form(...),

    files: List[UploadFile] = File(...)

):

    if upload_type not in [
        "ams",
        "asset",
        "software"
    ]:

        return {
            "success": False,
            "message": "Invalid Upload Type"
        }

    if upload_type == "ams" and len(files) != 2:

        return {
            "success": False,
            "message": "Please upload exactly one Incident file and one Request file."
        }

    if upload_type in ["asset", "software"] and len(files) != 1:

        return {
            "success": False,
            "message": "Only one file allowed."
        }

    saved_paths = []

    # =====================================================
    # SAVE FILES
    # =====================================================

    for file in files:

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if upload_type == "ams":
            save_path = RAW_FOLDER / file.filename
        else:
            save_path = RAW_FOLDER / f"{timestamp}_{file.filename}"

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_paths.append(save_path)

        print(f"Saved : {save_path.name}")

    # =====================================================
    # PROCESS
    # =====================================================

    try:

        incident_summary = None
        request_summary = None

        # =====================================================
        # AMS
        # =====================================================

        if upload_type == "ams":

            for file in saved_paths:

                report = get_report_type(file)

                print(f"\nDetected Report : {report}")
                print(f"File            : {file.name}")

                if report == "incident":

                    incident_summary = append_incident_master(file)

                elif report == "request":

                    request_summary = append_request_master(file)

                else:

                    return {
                        "success": False,
                        "message": f"Unknown report format : {file.name}"
                    }

            if incident_summary is None:
                return {
                    "success": False,
                    "message": "Incident file not found."
                }

            if request_summary is None:
                return {
                    "success": False,
                    "message": "Request file not found."
                }

            print("\n======================================")
            print("Running step2_ticket_master.py")
            print("======================================")

            subprocess.run(
                [
                    "python",
                    str(AMS_SCRIPT)
                ],
                check=True
            )

            print("\n======================================")
            print("Running step1_aggregation.py")
            print("======================================")

            subprocess.run(
                [
                    "python",
                    str(AGG_SCRIPT)
                ],
                check=True
            )

            return {

                "success": True,

                "message": "AMS Upload Successful",

                "incident": incident_summary,

                "request": request_summary

            }

        # =====================================================
        # ASSET
        # =====================================================

        if upload_type == "asset":

            subprocess.run(
                [
                    "python",
                    str(ASSET_SCRIPT)
                ],
                check=True
            )

            return {

                "success": True,

                "message": "Asset uploaded successfully."

            }

        # =====================================================
        # SOFTWARE
        # =====================================================

        subprocess.run(
            [
                "python",
                str(SOFTWARE_SCRIPT)
            ],
            check=True
        )

        return {

            "success": True,

            "message": "Software uploaded successfully."

        }

    except Exception as e:

     import traceback

     print("\n========== FULL ERROR ==========")
     traceback.print_exc()
     print("===============================\n")

     return {
        "success": False,
        "message": str(e)
     }


        # =====================================================
# GET UPLOADED FILES
# =====================================================

@router.get("/uploads")
def get_uploaded_files():

    files = []

    for file in RAW_FOLDER.glob("*"):

        if file.is_file():

            stat = file.stat()

            files.append({

                "file_name": file.name,

                "size_mb": round(
                    stat.st_size / (1024 * 1024),
                    2
                ),

                "upload_date": datetime.fromtimestamp(
                    stat.st_mtime
                ).strftime("%d %b %Y"),

                "timestamp": stat.st_mtime,

                "status": "Success"

            })

    files.sort(
        key=lambda x: x["timestamp"],
        reverse=True
    )

    for item in files:
        item.pop("timestamp")

    return files