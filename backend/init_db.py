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

def initialize_with_sql_script():
    """Initialize database using the PostgreSQL SQL script"""
    print("Initializing database with PostgreSQL schema...")
    
    database_url = Config.SQLALCHEMY_DATABASE_URI
    engine = create_engine(database_url)
    
    # Read and execute the PostgreSQL schema
    sql_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'PostgreDB.sql')
    
    if os.path.exists(sql_file_path):
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            
        # Execute the SQL script
        with engine.connect() as connection:
            # Split by statements (simple approach)
            statements = sql_content.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        connection.execute(statement)
                        connection.commit()
                    except Exception as e:
                        print(f"Warning: Could not execute statement: {e}")
        
        print("✅ Database initialized with SQL schema!")
    else:
        print("❌ SQL schema file not found, falling back to SQLAlchemy creation")
        create_tables()

if __name__ == "__main__":
    create_tables()
