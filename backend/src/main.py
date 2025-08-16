
# import os
# import uuid
# import webbrowser
# import threading
# from pathlib import Path
# from fastapi import FastAPI, Form, UploadFile, File, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# import uvicorn

# from .extractor import extract

# # --- Main Application Setup ---
# app = FastAPI()

# # --- Find the frontend folder's path ---
# # This goes from "backend/src/main.py" up to the project root and then into "frontend"
# frontend_path = Path(__file__).parent.parent.parent / "frontend"

# # --- Mount the Static Files (like index.html) ---
# app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# # --- API Endpoint to process documents (no changes here) ---
# @app.post("/extract_from_doc")
# async def extract_from_doc(
#     file_format: str = Form(...),
#     file: UploadFile = File(...),
# ):
#     upload_dir = "uploads"
#     os.makedirs(upload_dir, exist_ok=True)
#     file_path = os.path.join(upload_dir, f"{uuid.uuid4()}.pdf")
    
#     with open(file_path, "wb") as f:
#         contents = await file.read()
#         f.write(contents)

#     try:
#         data = extract(file_path, file_format)
#     except Exception as e:
#         data = {
#             'error': str(e)
#         }
#     finally:
#         if os.path.exists(file_path):
#             os.remove(file_path)

#     return data

# # --- New Endpoint to Serve the HTML Frontend ---
# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     # Reads the content of index.html and returns it
#     with open(frontend_path / "index.html", "r") as f:
#         html_content = f.read()
#     return HTMLResponse(content=html_content, status_code=200)

# # --- Logic to Run the App and Open Browser ---
# def open_browser():
#     """Opens the default web browser to the application's URL."""
#     webbrowser.open("http://127.0.0.1:8000")

# if __name__ == "__main__":
#     # Use a timer to open the browser 1 second after the server starts
#     threading.Timer(1, open_browser).start()
    
#     # Run the Uvicorn server
#     uvicorn.run(app, host="127.0.0.1", port=8000)
import os
import uuid
import webbrowser
import threading
from pathlib import Path
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from .extractor import extract

# --- Main Application Setup ---
app = FastAPI()

# --- Find the frontend folder's path ---
frontend_path = Path(__file__).parent.parent.parent / "frontend"

# --- Mount the Static Files (like style.css and script.js) ---
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# --- API Endpoint to process documents ---
@app.post("/extract_from_doc")
async def extract_from_doc(
    file_format: str = Form(...),
    file: UploadFile = File(...),
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{uuid.uuid4()}.pdf")
    
    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    try:
        data = extract(file_path, file_format)
    except Exception as e:
        data = {
            'error': str(e)
        }
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

    return data

# --- New Endpoint to Serve the HTML Frontend ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Reads the content of index.html using UTF-8 encoding
    with open(frontend_path / "index.html", "r", encoding="utf-8") as f: # <-- THIS LINE IS CORRECTED
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# --- Logic to Run the App and Open Browser ---
def open_browser():
    """Opens the default web browser to the application's URL."""
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)