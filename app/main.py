from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.utils import generate_short_code

app = FastAPI()

# In-memory store — simple dictionary for now
db = {}

class URLRequest(BaseModel):
    url: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/shorten")
def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    db[short_code] = request.url
    return {"short_code": short_code, "short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    url = db.get(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url=url)
