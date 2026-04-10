from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.api import router as api_router
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

# Serve the frontend from the repository root
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

app.include_router(api_router)
