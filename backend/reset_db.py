"""
Database reset script - drops existing tables and recreates them
"""
import asyncio
from sqlalchemy import text
from app.core.database import engine, Base

async def reset_database():
    """Drop all tables and recreate them"""
    print("🔄 Resetting database schema...")
    
    # Drop all tables
    async with engine.begin() as conn:
        # Drop with CASCADE to handle foreign keys
        await conn.execute(text("DROP TABLE IF EXISTS lead_purchases CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS lead_matches CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS tenant_leads CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS agents CASCADE"))
        print("✅ Dropped existing tables")
        
        # Recreate all tables with new schema
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Created new tables with updated schema")
    
    print("✅ Database reset complete!")

if __name__ == "__main__":
    asyncio.run(reset_database())
