import os


class Config:
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DATABASE_URL = os.environ.get("MMS_DATABASE_URL")

class TestingConfig(Config):
    DATABASE_URL = "sqlite:///:memory:"
