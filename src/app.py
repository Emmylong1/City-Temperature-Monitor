from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import asyncio
import os

from lib.temperature_scraper import scrape_temperatures
from lib.db import get_temperatures, init_schema

app = FastAPI(title="Temperature Data Collection System")

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

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    # Initialize database schema
    await init_schema()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/temperatures")
async def get_temperature_data():
    """Get temperature data from the database"""
    try:
        temperatures = await get_temperatures(limit=1000)
        return temperatures
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch temperature data: {str(e)}")

@app.get("/api/manual-scrape")
async def manual_scrape():
    """Manually trigger temperature scraping"""
    try:
        results = await scrape_temperatures()
        return {
            "success": True,
            "message": "Temperature scraping completed successfully",
            "results": results
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Failed to scrape temperature data: {str(e)}"
            }
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    from lib.db import check_db_connection
    
    try:
        # Check database connection
        await check_db_connection()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": f"Database connection failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
