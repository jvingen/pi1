import redis

from .data import DEFAULT_DB, DEFAULT_HOST, DEFAULT_PORT


def connect(
    host: str | None = None,
    port: int | None = None,
    db: int | None = None,
):
    if host is None:
        host = DEFAULT_HOST
    if port is None:
        port = DEFAULT_PORT
    if db is None:
        db = DEFAULT_DB
    pool = redis.ConnectionPool(host=host, port=port, db=db)
    return redis.Redis(connection_pool=pool)
