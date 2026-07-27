import pytest
from src.cache.redis import redis_manager
from src.rag.providers.pgvector_provider import get_vector_provider
from src.security.oauth import create_access_token


@pytest.mark.asyncio
async def test_redis_cache_set_and_get():
    await redis_manager.set("test_key", "test_val", ttl_seconds=10)
    val = await redis_manager.get("test_key")
    assert val == "test_val"


@pytest.mark.asyncio
async def test_jwt_token_generation_and_validation():
    token = create_access_token({"sub": "user_doc_99", "role": "physician"})
    assert token is not None and len(token) > 10


@pytest.mark.asyncio
async def test_pluggable_vector_provider_abstraction():
    provider = get_vector_provider("pgvector")
    assert provider is not None
