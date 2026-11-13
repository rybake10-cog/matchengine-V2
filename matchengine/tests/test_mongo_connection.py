import asyncio
from unittest import TestCase

from matchengine.internals.database_connectivity.mongo_connection import MongoDBConnection
from matchengine.internals.typing.matchengine_types import Secrets


def _connection(read_only=True, async_init=False, **secret_overrides):
    secrets = dict(host="db.example.org", port=10255, db="matchminer", auth_db="admin",
                   ro_username="reader", ro_password="p@ss:word/1", rw_username="writer",
                   rw_password="w#rite", replica_set=False, max_pool_size=False, min_pool_size=False)
    secrets.update(secret_overrides)

    class _Connection(MongoDBConnection):
        pass

    _Connection.secrets = Secrets(**secrets)
    return _Connection(read_only=read_only, async_init=async_init)


class TestMongoConnection(TestCase):
    def test_credentials_are_url_encoded(self):
        conn = _connection()
        db = conn.__enter__()
        try:
            assert conn.uri == "mongodb://reader:p%40ss%3Aword%2F1@db.example.org:10255/matchminer?authSource=admin"
            assert db.name == "matchminer"
        finally:
            conn.__exit__(None, None, None)

    def test_read_write_uses_rw_credentials(self):
        conn = _connection(read_only=False)
        conn.__enter__()
        try:
            assert conn.uri.startswith("mongodb://writer:w%23rite@")
        finally:
            conn.__exit__(None, None, None)

    def test_tls_and_retry_writes_for_cosmos_db(self):
        conn = _connection(tls=True, retry_writes=False)
        conn.__enter__()
        try:
            assert conn.uri.endswith("?authSource=admin&tls=true&retryWrites=false")
        finally:
            conn.__exit__(None, None, None)

    def test_tls_and_retry_writes_omitted_by_default(self):
        conn = _connection()
        conn.__enter__()
        try:
            assert "tls" not in conn.uri and "retryWrites" not in conn.uri
        finally:
            conn.__exit__(None, None, None)

    def test_async_connection_requires_aclose(self):
        conn = _connection(async_init=True)
        db = conn.__enter__()
        assert type(db).__name__ == "AsyncDatabase"
        with self.assertRaises(TypeError):
            conn.__exit__(None, None, None)
        asyncio.run(conn.aclose())
