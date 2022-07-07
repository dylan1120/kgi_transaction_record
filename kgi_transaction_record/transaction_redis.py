import numpy as np
import pandas as pd
import redis
import time
import datetime
from datetime import timezone, timedelta
import config


class RedisTime:
    def redis_set_time_kgi(self):
        time_now = float(time.time())
        time_now = time_now + 60 * 60 * 8
        pool = redis.ConnectionPool(
            host=config.redis["host"], port=config.redis["port"], decode_responses=True
        )
        r = redis.Redis(connection_pool=pool)
        r.set("kgi_time", time_now)

    def redis_get_time_kgi(self):
        pool = redis.ConnectionPool(
            host=config.redis["host"], port=config.redis["port"], decode_responses=True
        )
        r = redis.Redis(connection_pool=pool)
        today_date = datetime.datetime.now()
        today_date = today_date.astimezone(timezone(timedelta(hours=8)))
        today_date = today_date.strftime("%Y-%m-%d")
        today_time = time.strptime(today_date, "%Y-%m-%d")
        today_timestamp = time.mktime(today_time)
        if r.get("kgi_time") == None:
            r.set("kgi_time", 0)
        else:
            pass
        if float(r.get("kgi_time")) <= float(today_timestamp):
            r.set("kgi_time", today_timestamp)
        else:
            pass
        return float(r.get("kgi_time"))

    def time_to_seconds_kgi(self, input):
        ts = input.split(" ")
        if len(ts) == 5:
            datetime_datetime = datetime.datetime.strptime(
                ts[2] + "-" + ts[1] + "-" + ts[0] + "-" + ts[3], "%Y-%b-%d-%X"
            )
            seconds = time.mktime(datetime_datetime.timetuple())
        else:
            datetime_datetime = datetime.datetime.strptime(
                ts[3] + "-" + ts[2] + "-" + ts[1] + "-" + ts[4], "%Y-%b-%d-%X"
            )
            seconds = time.mktime(datetime_datetime.timetuple()) + 60 * 60 * 8
        return seconds
