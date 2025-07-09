#!/usr/bin/env python3
"""
Database initialization script for SchedulesApp
Creates all necessary tables and sets up the database schema
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from app.infrastructure.database import Base
from app.config import Config

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    # Get database URL from config
    database_url = Config.SQLALCHEMY_DATABASE_URI
    print(f"Connecting to database: {database_url}")
    
    # Create engine
    engine = create_engine(database_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables created successfully!")
    print("Tables created:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")

if __name__ == "__main__":
    create_tables()
