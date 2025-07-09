# SchedulesApp Backend Documentation

## Overview

The SchedulesApp backend is designed to manage the scheduling and management of security personnel across multiple buildings. It provides a robust API for handling various functionalities such as user authentication, shift management, and reporting.

## Project Structure

The backend is organized into several modules, each responsible for different aspects of the application:

- **Application Layer**: Contains services that handle business logic and application workflows.
  - `app/application/services.py`: Service classes and functions.
  
- **Domain Layer**: Defines the core data models of the application.
  - `app/domain/models.py`: Data models for entities like Vigilante, Turno, and Edificio.
  
- **Infrastructure Layer**: Manages external integrations and database connections.
  - `app/infrastructure/database.py`: Database management and ORM configurations.
  - `app/infrastructure/odoo_api.py`: Functions for interacting with the Odoo API.
  - `app/infrastructure/celery_worker.py`: Setup for handling asynchronous tasks with Celery.
  
- **Interface Layer**: Provides the API for external communication.
  - `app/interface/api/routes.py`: API routes and endpoints.
  - `app/interface/api/auth.py`: Authentication-related routes and JWT management.
  - `app/interface/schemas.py`: Data validation schemas.

## Installation

To set up the backend, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the backend directory:
   ```
   cd SchedulesApp/backend
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database and run migrations (if applicable).

5. Start the application:
   ```
   python app/main.py
   ```

## Configuration

Configuration settings are managed in `app/config.py`. Update the following settings as needed:

- Database URL
- Secret keys for JWT
- Other environment-specific settings

## Usage

The backend provides a RESTful API for interacting with the application. Refer to the API documentation for details on available endpoints and their usage.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.