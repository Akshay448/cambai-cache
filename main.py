from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
import redis
from redis.exceptions import RedisError
from tenacity import retry, stop_after_attempt, wait_fixed

from huey_config import create_key_with_huey, update_key_with_huey, delete_key_with_huey

app = FastAPI()
url = "redis://redis-kv-service:6379"


def get_redis_client():
    try:
        return redis.Redis.from_url(url, decode_responses=True)
    except RedisError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
def startup_event():
    # Test Redis connection at startup
    client = get_redis_client()
    if not client.ping():
        raise HTTPException(status_code=500, detail="Redis service is unavailable")


class KeyValue(BaseModel):
    key: str
    value: str


@app.post("/create/{key}")
def create_key(key: str, value: str = Query(..., description="The value to store with the key"),
               redis_client: redis.Redis = Depends(get_redis_client)):
    result = create_key_with_huey(key, value)
    return {"message": "Task submitted", "task_id": result.id}


@app.get("/read/{key}")
def read_key(key: str, redis_client: redis.Redis = Depends(get_redis_client)):
    value = retry_read_key(redis_client, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def retry_read_key(redis_client, key):
    try:
        return redis_client.get(key)
    except RedisError:
        # This will automatically retry for transient errors
        raise


@app.put("/update/{key}")
def update_key(key: str, value: str = Query(..., description="The new value for the key")):
    result = update_key_with_huey(key, value)
    return {"message": "Task submitted", "task_id": result.id}


@app.delete("/delete/{key}")
def delete_key(key: str):
    result = delete_key_with_huey(key)
    return {"message": "Task submitted", "task_id": result.id}
