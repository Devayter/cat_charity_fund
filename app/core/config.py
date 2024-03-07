from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'APP_TITLE'
    app_description: str = 'APP_DESCRIPTION'
    database_url: str = 'sqlite+aiosqlite:///./charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
