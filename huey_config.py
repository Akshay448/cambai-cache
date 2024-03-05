from huey import RedisHuey
import redis
from redis.exceptions import RedisError

huey = RedisHuey('my_app', host='redis-huey-service', port=6379)
redis_client = redis.Redis(host='redis-kv-service', port=6379, decode_responses=True)


@huey.task()
def create_key_with_huey(key, value):
    try:
        if redis_client.exists(key):
            return {"status": "error", "message": "Key already exists"}
        redis_client.set(key, value)
        return {"status": "success", "message": "Key created successfully"}
    except RedisError as e:
        return {"status": "error", "message": str(e)}


@huey.task()
def update_key_with_huey(key, value):
    try:
        if not redis_client.exists(key):
            return {"status": "error", "message": "Key not found"}
        redis_client.set(key, value)
        return {"status": "success", "message": "Key updated successfully"}
    except RedisError as e:
        return {"status": "error", "message": str(e)}


@huey.task()
def delete_key_with_huey(key):
    try:
        if not redis_client.exists(key):
            return {"status": "error", "message": "Key not found"}
        redis_client.delete(key)
        return {"status": "success", "message": "Key deleted successfully"}
    except RedisError as e:
        return {"status": "error", "message": str(e)}
