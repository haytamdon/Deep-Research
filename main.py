from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import messages
from starlette.middleware.base import BaseHTTPMiddleware

# Initialize the FastAPI app
app = FastAPI(
    title="API for deep search",
    description="A backend API for deep search.",
    version="1.0.0",
    redirect_slashes=True
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Include routers
app.include_router(messages.router, prefix="/messages", tags=["Messages"])

# Health check endpoint
@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "OK", "message": "foldrAI.com API is running."}