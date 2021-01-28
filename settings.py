import os
import sys

from pydantic import BaseSettings
import logging

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(ROOT_DIR, 'apis')
sys.path.append(ROOT_DIR)
sys.path.append(BASE_DIR)


class Settings(BaseSettings):
    sqlalchemy_url: str = f"sqlite:///{BASE_DIR}/database.db"

    class Config:
        env_file = ".env"


settings = Settings()


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
