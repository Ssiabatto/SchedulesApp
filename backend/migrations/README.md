# README for Migrations

This directory contains the migration scripts for the database schema of the SchedulesApp project. 

## Overview

Database migrations are essential for managing changes to the database schema over time. They allow you to:

- Track changes to the database structure.
- Apply updates to the database schema in a controlled manner.
- Roll back changes if necessary.

## Migration Tools

This project uses **Flask-Migrate**, which is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. 

## Commands

To manage migrations, you can use the following commands:

- **Initialize migrations**: 
  ```
  flask db init
  ```

- **Create a new migration**: 
  ```
  flask db migrate -m "Description of changes"
  ```

- **Apply migrations**: 
  ```
  flask db upgrade
  ```

- **Rollback migrations**: 
  ```
  flask db downgrade
  ```

## Best Practices

- Always create a migration after making changes to the models.
- Review the generated migration scripts before applying them to ensure they reflect the intended changes.
- Test migrations in a development environment before applying them to production.

## Additional Resources

For more information on Flask-Migrate and Alembic, refer to the official documentation:

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/en/latest/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)