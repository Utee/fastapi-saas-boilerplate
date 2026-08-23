from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI SaaS Boilerplate"
    API_V1_STR: str = "/api/v1"
    
    # Injected automatically by Railway
    DATABASE_URL: str
    REDIS_URL: str
    
    # Generated on template deployment
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # User-provided on deployment
    STRIPE_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()