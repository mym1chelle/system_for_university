from dataclasses import dataclass
from environs import Env


@dataclass
class DataBaseConfig:
    uri: str
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class Config:
    db: DataBaseConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        db=DataBaseConfig(
            uri=env.str('DB_URI'),
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.str('DB_PORT')
        )
    )