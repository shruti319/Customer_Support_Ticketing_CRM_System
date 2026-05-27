
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from database import engine, Base
from routers import tickets


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    print("Starting Support CRM...")
    Base.metadata.create_all(bind=engine)
    print("Database tables ready")
    yield  # App runs here
    print("Shutting down Support CRM...")


# Create the FastAPI app
app = FastAPI(
    title="Support CRM",
    description="Customer Support Ticketing System — Datastraw Assessment",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(tickets.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


#PAGE ROUTES 
@app.get("/")
def home():
    """Serves the home page (ticket list)"""
    return FileResponse("static/index.html")


@app.get("/create")
def create_page():
    """Serves the create ticket form page"""
    return FileResponse("static/create.html")


@app.get("/ticket/{ticket_id}")
def ticket_detail_page(ticket_id: str):
    """Serves the ticket detail page"""
    return FileResponse("static/ticket.html")


#HEALTH CHECK
@app.get("/health")
def health_check():
    """Simple endpoint to verify the server is running. Railway uses this."""
    return {"status": "ok", "message": "Support CRM is running"}
