"""
FastAPI application for Strategic Intelligence API
"""
from fastapi import FastAPI

app = FastAPI(title="Strategic Intelligence API")

@app.get("/health")
def health():
    return {"status": "healthy"}
