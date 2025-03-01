import uvicorn
from fastapi import FastAPI
from ai_backend.routers import chat

app = FastAPI(title="AI Backend API")

# Register routers
app.include_router(chat.router, prefix="/api")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Backend is running"}


def start():
    """Entry point for Poetry script to launch the Uvicorn server."""
    uvicorn.run("ai_backend.main:app", host="0.0.0.0", port=8080, reload=True)
