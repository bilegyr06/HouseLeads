"""
Database reset script - drops existing tables and recreates them
"""
import asyncio
import subprocess
import sys
from pathlib import Path
from sqlalchemy import text
from app.core.database import engine

async def reset_database():
    """Drop all tables and recreate them using Alembic migrations."""
    print("🔄 Resetting database schema...")
    
    # Drop all tables
    async with engine.begin() as conn:
        # Drop with CASCADE to handle foreign keys
        await conn.execute(text("DROP TABLE IF EXISTS lead_purchases CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS lead_matches CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS tenant_leads CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS agents CASCADE"))
        print("✅ Dropped existing tables")
    
    backend_dir = Path(__file__).resolve().parent
    alembic_ini = backend_dir / "alembic.ini"
    print("🗄️  Recreating schema with Alembic migrations...")
    subprocess.run(
        [sys.executable, "-m", "alembic", "-c", str(alembic_ini), "upgrade", "head"],
        check=True,
        cwd=str(backend_dir),
    )
    print("✅ Created new tables with Alembic")

    print("✅ Database reset complete!")

if __name__ == "__main__":
    asyncio.run(reset_database())
