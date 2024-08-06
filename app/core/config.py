from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str = ('Описание')

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
