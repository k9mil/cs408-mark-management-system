import os


class Config:
    pass

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DATABASE_URL = os.environ.get("MMS_DATABASE_URL")