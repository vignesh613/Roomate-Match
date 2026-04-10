from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.api import router as api_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Roommate Matching Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("../frontend/index.html")

@app.get("/index.html")
async def serve_index():
    return FileResponse("../frontend/index.html")

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Roommate Matching API"}