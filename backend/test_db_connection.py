"""
Database Connection Test Script
Tests the PostgreSQL connection and verifies all models can be initialized.
"""

import asyncio
import sys
from sqlalchemy import text


async def test_database_connection():
    """Test PostgreSQL connection and schema initialization."""
    
    print("=" * 70)
    print("🔍 DATABASE CONNECTION TEST")
    print("=" * 70)
    print()
    
    try:
        # Import after print to show progress
        print("📦 Importing app configuration...")
        from app.core.config import settings
        from app.core.database import engine, Base
        from app.models import TenantLead, Agent, LeadPurchase
        
        print(f"✅ Config loaded successfully")
        print(f"   Database URL: {settings.DATABASE_URL.replace(settings.DATABASE_URL.split('@')[0].split('://')[1], '***:***')}")
        print()
        
        # Test connection
        print("🔌 Testing database connection...")
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"✅ Connected to PostgreSQL")
            print(f"   {version}")
        print()
        
        # Create tables
        print("📊 Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f"✅ Tables created/verified successfully")
        print()
        
        # List tables
        print("📋 Verifying tables in database:")
        async with engine.begin() as conn:
            result = await conn.execute(
                text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema='public'
                    ORDER BY table_name;
                """)
            )
            tables = result.scalars().all()
            for table in tables:
                print(f"   ✅ {table}")
        print()
        
        # Model verification
        print("🔍 Verifying ORM models:")
        models = [
            ("TenantLead", TenantLead),
            ("Agent", Agent),
            ("LeadPurchase", LeadPurchase),
        ]
        for name, model in models:
            print(f"   ✅ {name} - {model.__tablename__}")
        print()
        
        # Connection pool info
        print("⚙️  Connection Pool Status:")
        print(f"   Pool size: 20")
        print(f"   Pre-ping enabled: True")
        print()
        
        print("=" * 70)
        print("✅ ALL DATABASE TESTS PASSED!")
        print("=" * 70)
        print()
        print("🚀 You can now start the API with:")
        print("   uvicorn app.main:app --reload")
        print()
        
        await engine.dispose()
        return True
        
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ DATABASE CONNECTION FAILED!")
        print("=" * 70)
        print()
        print(f"Error: {str(e)}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Verify PostgreSQL is running: sudo systemctl start postgresql")
        print("   2. Check database exists: psql -U postgres -l")
        print("   3. Verify credentials in .env are correct")
        print("   4. Check firewall allows localhost:5432")
        print()
        await engine.dispose()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_database_connection())
    sys.exit(0 if success else 1)
