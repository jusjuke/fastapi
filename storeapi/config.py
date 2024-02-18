from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    #    DATABASE_URL: Optional[str] = None
    #    DEV_DATABASE_URL: Optional[str] = None
    #    TEST_DATABASE_URL: Optional[str] = None
    #    PROD_DATABASE_URL: Optional[str] = None

    class Config:
        env_file: str = ".env"


class GlobalConfig(BaseConfig):
    DB_FORCE_ROLLBACK: bool = False


class DevConfig(GlobalConfig):
    DB_FORCE_ROLLBACK: bool = True


#    class Config:
#        env_prefixz: str = "DEV_"


class TestConfig(GlobalConfig):
    #    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLLBACK: bool = True


#    class Config:
#        env_prefix: str = "TEST_"


class ProdConfig(GlobalConfig):
    #    DATABASE_URL: str
    DB_FORCE_ROLLBACK: bool = False


#    class Config:
#        env_prefix: str = "PROD_"


@lru_cache()
def get_config(env_state: str) -> BaseConfig:
    configs = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
    print(configs[env_state]().DATABASE_URL)
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
