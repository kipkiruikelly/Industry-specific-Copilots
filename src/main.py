import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MediCopilot Healthcare AI Platform",
    openapi_url="/api/v1/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "healthy", "service": "MediCopilot Healthcare AI Platform"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Lazy load API router inside startup or on demand if dependencies allow
try:
    from src.api.router import api_router
    app.include_router(api_router, prefix="/api/v1")
except Exception as e:
    print(f"Warning: Deferred full router initialization: {e}")

if __name__ == "__main__":
    port_str = os.getenv("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
