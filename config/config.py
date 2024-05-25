from dataclasses import dataclass
from dotenv import dotenv_values


@dataclass
class Settings:
    JWTSecret: str
    JWTAlgo: str
    DatabaseURL: str


setting = Settings


def initialize_settings(env_file: str | None = None):
    """
    Initialize the application with the env file. Contains information used across the app.
    If no env_file parameter is passed in, env file defaults to '.env'
    :param env_file:
    :return:
    """
    if env_file is None:
        env_file = ".env"

    env = dotenv_values(env_file)
    setting.JWTAlgo = env.get("JWT_Algo")
    setting.JWTSecret = env.get("JWT_SECRET")
    setting.DatabaseURL = env.get("DB_URL")
