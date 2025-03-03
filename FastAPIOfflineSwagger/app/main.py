from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import zipfile
import threading

import subprocess

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
import fastapi_offline_swagger_ui
from os import path
import pathlib

app = FastAPI()

static_dir = pathlib.Path(__file__).parent / "static"

# Mount the directory containing Swagger UI assets
if path.exists(static_dir / "swagger-ui.css") and path.exists(static_dir / "swagger-ui-bundle.js"):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print("mounted")

# Override the default Swagger UI HTML generation to use local assets
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_favicon_url="",
        swagger_css_url="/assets/swagger-ui.css",
        swagger_js_url="/assets/swagger-ui-bundle.js",
    )

# Replace the default Swagger UI HTML generation method

@app.get("/")
async def index():
    return FileResponse(static_dir / 'index.html', media_type='text/html')

app.get("/docs", include_in_schema=True)(swagger_monkey_patch)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=10001)

