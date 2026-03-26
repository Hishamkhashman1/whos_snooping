from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from scanner import get_local_subnet, scan_network  # noqa: E402


class Device(BaseModel):
    ip: str
    mac: str
    vendor: str
    hostname: Optional[str] = None


class ScanResponse(BaseModel):
    subnet: str
    devices: List[Device]


app = FastAPI(title="Who's Snooping API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/scan", response_model=ScanResponse)
def scan():
    try:
        subnet = get_local_subnet()
        devices = scan_network(subnet)
    except PermissionError:
        raise HTTPException(
            status_code=500,
            detail="Permission denied. Run the API with sudo or grant raw socket access.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {"subnet": subnet, "devices": devices}
