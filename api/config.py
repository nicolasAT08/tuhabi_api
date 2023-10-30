import os
from dotenv import load_dotenv
load_dotenv()

# Set environment variables
class Settings(object):
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    user = os.environ.get("USER")
    passwordd = os.environ.get("PASSWORD")
    database = os.environ.get("DATABASE")
    secret_key = os.environ.get("SECRET_KEY")
    algorithm = os.environ.get("ALGORITHM")
    access_token_expire_minutes = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = '.env'

settings = Settings()