import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://localhost/spacer")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
    SWAGGER = {
        "title": "Spacer API",
        "uiversion": 3
    }
    # Email configuration
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True") == "True"
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")
    
    # Cloudinary configuration
    CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    
    # CORS configuration
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    
    # Redis/Cache configuration
    CACHE_TYPE = os.getenv("CACHE_TYPE", "redis")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))
    
    # Rate Limiting
    RATELIMIT_DEFAULT = os.getenv("RATELIMIT_DEFAULT", "200 per day")
    
    # Other settings
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16777216))
    ALLOWED_IMAGE_EXTENSIONS = os.getenv("ALLOWED_IMAGE_EXTENSIONS", "png,jpg,jpeg,gif").split(",")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TESTING = os.getenv("TESTING", "False") == "True"
