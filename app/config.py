from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_name: str
    database_username: str
    database_pswrd: str
    database_hostname: str
    database_portname: str
    algorithm: str
    secret_key: str
    algorithm_exp_min: int

    model_config = SettingsConfigDict(env_file=".env")

settings=Settings()