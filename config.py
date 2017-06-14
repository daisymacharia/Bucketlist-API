import os
class Config(object):
    """Parent configuration class."""
    DEBUG = False
    
class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_bucket_list_api'
    DEBUG = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
