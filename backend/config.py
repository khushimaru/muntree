import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', "supersecret")
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES', 10080))
DATABASE_URL = os.getenv('DATABASE_URL', "sqlite:///./db.sqlite")
ADMIN_REGISTRATION_KEY = os.getenv('ADMIN_REGISTRATION_KEY', "key")