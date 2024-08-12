from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str
    database_url: str
    secret: str = 'SECRET'

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
