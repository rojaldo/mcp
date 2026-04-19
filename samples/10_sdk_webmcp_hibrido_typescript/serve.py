from __future__ import annotations

from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
WEB_DIR = BASE_DIR / "web"
DIST_DIR = WEB_DIR / "dist"

app = FastAPI(title="webmcp-hibrido-demo")

if DIST_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=DIST_DIR), name="static")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    uvicorn.run("serve:app", host="127.0.0.1", port=8000, reload=True)
