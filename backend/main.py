from fastapi import FastAPI
from app.routers import api_router
from app import models
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv()

app = FastAPI()
app.include_router(api_router)

origins = os.getenv("FRONTEND_ORIGINS","").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)