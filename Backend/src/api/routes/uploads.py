from fastapi import APIRouter, UploadFile, File, Form
from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import subprocess
import pandas as pd

router = APIRouter()

# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

RAW_FOLDER = BASE_DIR / "data" / "raw"
MASTER_FOLDER = BASE_DIR / "data" / "Master"

RAW_FOLDER.mkdir(parents=True, exist_ok=True)
MASTER_FOLDER.mkdir(parents=True, exist_ok=True)

# Pipeline scripts
PIPELINE_FOLDER = BASE_DIR / "src" / "pipeline"

AMS_SCRIPT = PIPELINE_FOLDER / "step2_ticket_master.py"
AGG_SCRIPT = PIPELINE_FOLDER / "step1_aggregation.py"
ASSET_SCRIPT = PIPELINE_FOLDER / "Asset_count.py"
SOFTWARE_SCRIPT = PIPELINE_FOLDER / "software_requisition.py"


# --------------------------------------------------
# APPEND DATA TO MASTER FILE + REMOVE DUPLICATES
# --------------------------------------------------

def append_to_master(uploaded_file_path, master_file_path):

    print("\n========== APPEND DEBUG ==========")
    print("Uploaded path:", uploaded_file_path)
    print("Master path:", master_file_path)

    new_df = pd.read_excel(uploaded_file_path, dtype=str)

    print("Uploaded rows:", len(new_df))
    print("Uploaded columns:", list(new_df.columns))

    new_df.columns = [
        str(col).replace("\n", " ").strip()
        for col in new_df.columns
    ]

    if master_file_path.exists():
        old_df = pd.read_excel(master_file_path, dtype=str)

        print("Old master rows:", len(old_df))

        old_df.columns = [
            str(col).replace("\n", " ").strip()
            for col in old_df.columns
        ]

        combined_df = pd.concat(
            [old_df, new_df],
            ignore_index=True
        )
    else:
        combined_df = new_df

    before_count = len(combined_df)

    # --------------------------------------------------
    # DEDUPLICATION BASED ON UNIQUE KEYS
    # --------------------------------------------------

    if "Incident ID" in combined_df.columns:
        combined_df = combined_df.drop_duplicates(
            subset=["Incident ID"]
        )

    elif "Request ID" in combined_df.columns:
        combined_df = combined_df.drop_duplicates(
            subset=["Request ID"]
        )

    elif "RITM No" in combined_df.columns:
        combined_df = combined_df.drop_duplicates(
            subset=["RITM No"]
        )

    elif "RITM" in combined_df.columns:
        combined_df = combined_df.drop_duplicates(
            subset=["RITM"]
        )

    after_count = len(combined_df)

    print("Rows before dedupe:", before_count)
    print("Rows after dedupe:", after_count)
    print(f"Duplicates removed: {before_count - after_count}")
    print(f"Final rows in master: {after_count}")

    combined_df.to_excel(master_file_path, index=False)

    print("Saved successfully to:", master_file_path)


# --------------------------------------------------
# UPLOAD EXCEL
# --------------------------------------------------

@router.post("/upload-excel")
async def upload_excel(
    upload_type: str = Form(...),
    files: List[UploadFile] = File(...)
):

    if upload_type not in ["ams", "asset", "software"]:
        return {"success": False, "message": "Invalid upload type"}

    if upload_type == "ams" and len(files) != 2:
        return {"success": False, "message": "AMS requires exactly 2 files"}

    if upload_type in ["asset", "software"] and len(files) != 1:
        return {"success": False, "message": "Only 1 file allowed"}

    saved_paths = []

    # SAVE FILES
    for file in files:

        if not file.filename.endswith((".xlsx", ".xls")):
            return {
                "success": False,
                "message": "Only Excel files allowed"
            }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if upload_type == "asset":
            file_path = RAW_FOLDER / f"asset_{timestamp}_{file.filename}"

        elif upload_type == "software":
            file_path = RAW_FOLDER / f"software_{timestamp}_{file.filename}"

        else:
            file_path = RAW_FOLDER / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        saved_paths.append(file_path)

    try:

        # ==================================================
        # AMS
        # ==================================================
        if upload_type == "ams":

            incident_master = MASTER_FOLDER / "master_incidents.xlsx"
            request_master = MASTER_FOLDER / "master_requests.xlsx"

            for path in saved_paths:
                df = pd.read_excel(path, nrows=5)

                columns = [
                    str(col).replace("\n", " ").strip()
                    for col in df.columns
                ]

                if "Incident ID" in columns:
                    print(f"Incident file detected: {path.name}")
                    append_to_master(path, incident_master)

                elif "Request ID" in columns:
                    print(f"Request file detected: {path.name}")
                    append_to_master(path, request_master)

                else:
                    return {
                        "success": False,
                        "message": f"Unknown AMS file format: {path.name}"
                    }

            print("Running AMS pipeline...")
            subprocess.run(["python", str(AMS_SCRIPT)], check=True)
            subprocess.run(["python", str(AGG_SCRIPT)], check=True)

        # ==================================================
        # ASSET
        # ==================================================
        elif upload_type == "asset":

            asset_master = MASTER_FOLDER / "master_assets.xlsx"

            print("Asset master path:", asset_master.resolve())

            append_to_master(saved_paths[0], asset_master)

            print("Running Asset pipeline...")
            subprocess.run(["python", str(ASSET_SCRIPT)], check=True)

        # ==================================================
        # SOFTWARE
        # ==================================================
        elif upload_type == "software":

            software_master = MASTER_FOLDER / "master_software.xlsx"

            print("Software master path:", software_master.resolve())
            print("Saved paths:", saved_paths)

            append_to_master(saved_paths[0], software_master)

            verify_df = pd.read_excel(software_master)
            print("Rows immediately after append:", len(verify_df))

            print("Running Software pipeline...")
            subprocess.run(
                ["python", str(SOFTWARE_SCRIPT)],
                check=True
            )

            verify_df_after = pd.read_excel(software_master)
            print("Rows after pipeline:", len(verify_df_after))

        return {
            "success": True,
            "message": f"{upload_type.upper()} upload successful"
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
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

            files.append({
                "file_name": file.name,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "upload_date": datetime.fromtimestamp(
                    stat.st_mtime
                ).strftime("%d %b %Y"),
                "timestamp": stat.st_mtime,
                "status": "Success"
            })

    files.sort(
        key=lambda item: item["timestamp"],
        reverse=True
    )

    for item in files:
        item.pop("timestamp")

    return files