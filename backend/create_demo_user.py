#!/usr/bin/env python3
"""
Demo script to create a test user for the SchedulesApp
Run this script to create a sample user for testing the authentication system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from werkzeug.security import generate_password_hash
from app.application.services import UserService
from app.infrastructure.database import DatabaseSession, SQLUserRepository
from app.domain.models import User

def create_demo_user():
    """Create a demo user for testing"""
    
    # Initialize database and repositories (use environment variable or default)
    database_url = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/dbname')
    db_session = DatabaseSession(database_url)
    user_repository = SQLUserRepository(db_session)
    user_service = UserService(user_repository)
    
    # Demo user data
    demo_user_data = {
        'username': 'admin',
        'email': 'admin@schedules.app',
        'password': generate_password_hash('admin123'),  # Hash the password
        'full_name': 'Administrator',
        'role': 'operator'
    }
    
    print("Creating demo user...")
    print(f"Username: {demo_user_data['username']}")
    print(f"Email: {demo_user_data['email']}")
    print(f"Password: admin123")
    print(f"Role: {demo_user_data['role']}")
    
    result = user_service.register_user(demo_user_data)
    
    if result['success']:
        print("✅ Demo user created successfully!")
        print("You can now use the following credentials to login:")
        print("Username: admin")
        print("Password: admin123")
    else:
        print(f"❌ Failed to create demo user: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    create_demo_user()
