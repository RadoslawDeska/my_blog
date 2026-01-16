# Flask Blog Application

## Overview
A simple Flask-based blog application with user authentication, post creation/editing, and draft management.

## Project Structure
```
/
├── blog/
│   ├── __init__.py      # Flask app initialization
│   ├── forms.py         # WTForms form definitions
│   ├── handlers.py      # Request handlers
│   ├── models.py        # SQLAlchemy models
│   ├── routes.py        # URL routes
│   └── templates/       # Jinja2 templates
├── migrations/          # Alembic database migrations
├── config.py            # Application configuration
├── main.py              # Entry point
└── requirements.txt     # Python dependencies
```

## Technologies
- **Framework**: Flask 3.1.2
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Flask-Migrate (Alembic)
- **Forms**: Flask-WTF / WTForms
- **Templates**: Jinja2

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string (auto-configured)
- `SECRET_KEY` - Flask secret key for sessions
- `ADMIN_USERNAME` - Admin login username (default: "admin")
- `ADMIN_PASSWORD` - Admin login password (default: "change-me")

## Running the Application
The app runs on port 5000 via the "Start Flask App" workflow.

## Features
- Homepage showing published blog posts
- Admin login for post management
- Create, edit, and delete blog posts
- Draft management for unpublished posts

## Recent Changes
- 2026-01-16: Initial setup for Replit environment
  - Added PostgreSQL database support with psycopg2
  - Created main.py entry point
  - Configured workflow for port 5000
