import asyncio
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import engine, Base
from backend.app.models.user import User
from backend.app.models.property import Property
from backend.app.models.risk_assessment import RiskAssessment
from backend.app.models.scenario import Scenario
from backend.app.models.portfolio import Portfolio

async def test_database():
    print("Testing database connection...")
    
    # Test database connection
    try:
        connection = engine.connect()
        print("✅ Database connection successful")
        connection.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Create tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created")
    except Exception as e:
        print(f"❌ Database table creation failed: {e}")
        return
    
    # Test creating a user
    try:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create a test user
        test_user = User(
            email="test@example.com",
            hashed_password="hashed_password",
            first_name="Test",
            last_name="User",
            role="viewer"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ User created: {test_user.email}")
        
        # Query the user
        user = db.query(User).filter(User.email == "test@example.com").first()
        print(f"✅ User query successful: {user.email}")
        
        db.close()
    except Exception as e:
        print(f"❌ Database operations failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_database())