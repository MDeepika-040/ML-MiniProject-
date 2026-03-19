"""
Configuration settings for the Hypertension Prediction Application
"""

import os

class Config:
    """Base configuration"""
    
    # Flask Settings
    DEBUG = False
    TESTING = False
    
    # JWT Settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-this-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 30 * 24 * 60 * 60  # 30 days
    
    # Database
    DATABASE = 'hypertension.db'
    
    # CSV Data Path
    CSV_PATH = os.environ.get('CSV_PATH', r"C:\Users\karun\Downloads\hypertension_data.csv.zip")
    
    # CORS Settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Update these for production
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'CHANGE_ME_PRODUCTION_SECRET')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE = ':memory:'  # Use in-memory database for tests


# Select configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
