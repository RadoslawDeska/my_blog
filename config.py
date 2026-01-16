import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 1


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "remember-to-add-secret-key"
    )  # 2
    SQLALCHEMY_DATABASE_URI = (  # 3
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(BASE_DIR, "database.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Neon-specific connection pool settings (REPLIT)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,         # Test connections before using them
        "pool_recycle": 300,           # Recycle connections every 5 minutes
        "pool_size": 5,                # Limit concurrent connections
        "max_overflow": 2,             # Allow 2 extra connections if needed
        "pool_timeout": 30,            # Wait 30s for a connection from the pool
    }

    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me")

    # Cookie Security Settings
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript from accessing the session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # Helps prevent CSRF attacks
    
    # Only enable this if you're using HTTPS (you should in production!)
    # For local development on http://localhost, keep this False
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"