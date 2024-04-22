import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import csv_router, text_router

app = FastAPI()

# Enable CORS for all routes and origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add route handlers
app.include_router(csv_router, prefix="/api/anonymize/csv", tags=["CSV Anonymization"])
app.include_router(text_router, prefix="/api/anonymize/text", tags=["Text Anonymization"])

@app.get("/api")
def read_root():
    return {"message": "API is up and running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)