from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    @property
    def db_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_url_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# COOKIE_NAME = "access_token"
#
# models = AuthXConfig()
# models.JWT_SECRET_KEY = "SECRET_KEY"  # todo: вероятно его указывать нужно не здесь
# models.JWT_ACCESS_COOKIE_NAME = COOKIE_NAME
# models.JWT_TOKEN_LOCATION = ["headers"]
#
# security = AuthX(models=models)
