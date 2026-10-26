from fastapi import FastAPI
from pydantic import BaseModel
from extract import extract_validated

app = FastAPI()

class ExtractRequest(BaseModel):
    text: str

@app.post("/extract")
def extract_endpoint(req: ExtractRequest):
    return extract_validated(req.text)
