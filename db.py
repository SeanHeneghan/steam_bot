from dotenv import load_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings
from psycopg_pool import AsyncConnectionPool
from functools import lru_cache


load_dotenv()


class DatabaseInfo(BaseSettings):
    """Database to manage pools, info and connections."""

    scheme: str = Field("postgresql")
    host: str = Field(...)
    port: int = Field(...)
    user: str = Field(...)
    password: str = Field(...)
    dbname: str = Field(...)
    _pool: AsyncConnectionPool | None = None

    @property
    def uri(self) -> PostgresDsn:
        """Construct uri for connection."""
        return str(
            PostgresDsn.build(
                scheme=self.scheme,
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.dbname,
            )
        )

    @property
    def pool(self) -> AsyncConnectionPool:
        """Initialise connection pool if it does not exist."""
        if not self._pool:
            self._pool = AsyncConnectionPool(conninfo=self.uri, kwargs={"autocommit": True})
        return self._pool

    class Config:
        env_prefix = "POSTGRES_"
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache(maxsize=1)
def get_db_connection() -> DatabaseInfo:
    "Make db connection a singleton."
    return DatabaseInfo()
