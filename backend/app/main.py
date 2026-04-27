"""
FastAPI application entry point for HomeLeads API.
Initializes the FastAPI app, registers routers, sets up exception handlers,
and configures CORS for cross-origin requests.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import Base, engine
from app.routes import leads, agents, payments, auth


# Lifespan context manager for database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage app lifespan: initialize database tables on startup,
    clean up on shutdown.
    """
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables initialized")
    
    yield
    
    # Shutdown
    await engine.dispose()
    print("✅ Database connections closed")


# Initialize FastAPI app
app = FastAPI(
    title="HomeLeads API",
    description="Real estate lead matching and management platform for Nigeria",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors gracefully."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred. Please try again later."},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    if settings.DEBUG:
        # Return detailed error in development
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
    else:
        # Return generic error in production
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )


# ============================================================================
# Routes
# ============================================================================

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify API is running."""
    return {
        "status": "ok",
        "app": "HomeLeads API",
        "version": "1.0.0",
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "app": "HomeLeads API",
        "description": "Real estate lead matching and management platform",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi_schema": "/openapi.json",
    }


# Register API routers with v1 prefix
api_v1_prefix = "/api/v1"

app.include_router(
    auth.router,
    prefix=f"{api_v1_prefix}",
    tags=["Authentication"],
)

app.include_router(
    leads.router,
    prefix=f"{api_v1_prefix}",
    tags=["Leads"],
)

app.include_router(
    agents.router,
    prefix=f"{api_v1_prefix}",
    tags=["Agents"],
)

app.include_router(
    payments.router,
    prefix=f"{api_v1_prefix}",
    tags=["Payments"],
)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
