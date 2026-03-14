"""
Configuration management for the API
"""

import os
from pathlib import Path

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./fastapi_app.db")

# API configuration
API_PREFIX = "/api"
API_VERSION = "v1"

# CORS configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
