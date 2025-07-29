import redis
import json
import os
from datetime import datetime, timedelta


   
def init_redis(host=None, port=6379, db=0):
    """Подключение к Redis"""
    host = host or os.getenv("REDIS_HOST", "127.0.0.1")
    global client 
    client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)


def water_stats(user_id: int, amount: int):
    """Сохраняет потребление воды с разбивкой по дням"""
    
    daily_key = f"user:{user_id}:water:{datetime.now().strftime('%Y-%m-%d')}"
    weekly_key = f"user:{user_id}:water:week:{datetime.now().strftime('%Y-%U')}"
    
    # Pipeline для атомарного выполнения
    with client.pipeline() as pipe:
        pipe.incrby(daily_key, amount)
        pipe.expire(daily_key, 86400)  # TTL 1 день
        pipe.incrby(weekly_key, amount)
        pipe.expire(weekly_key, 604800)  # TTL 1 неделя
        pipe.execute()

def fan_stats(user_id: int, amount: int):
    """Сохраняет потребление воды с разбивкой по дням"""
    
    daily_key = f"user:{user_id}:fan:{datetime.now().strftime('%Y-%m-%d')}"
    weekly_key = f"user:{user_id}:fan:fan:{datetime.now().strftime('%Y-%U')}"

    with client.pipeline() as pipe:
        pipe.incrby(daily_key, amount)
        pipe.expire(daily_key, 86400)  # TTL 1 день
        pipe.incrby(weekly_key, amount)
        pipe.expire(weekly_key, 604800)  # TTL 1 неделя
        pipe.execute()