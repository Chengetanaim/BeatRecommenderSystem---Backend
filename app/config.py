from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    username: str
    password: str
    host_name: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
