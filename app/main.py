from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()

from app.db import Base, engine
from app.routes import invoices

app = FastAPI(title="Invoice Summarizer API")

@app.get("/")
def home():
    return {"message": "Server is running!!!"}

app.include_router(invoices.router)