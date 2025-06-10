from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse ,JSONResponse
from app.api.routers import news
from app.database.models import Base, engine
from fastapi.requests import Request

# Initialize Database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    print(f"404 for {request.url} from {request.headers.get('User-Agent')}")
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include news Router
app.include_router(news.router)

# Root endpoint to serve the homepage
@app.get("/", tags=["Root"])
async def root():
    return FileResponse("static/index.html")

# Run with: uvicorn main:app --reload
