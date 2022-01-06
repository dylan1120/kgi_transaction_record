import numpy as np
import pandas as pd
import redis
import time
import datetime

class RedisTime():
    def redis_set_time_kgi(self):
        time_now = float(time.time())
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        r.set('kgi_time',time_now)

    def redis_get_time_kgi(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        if r.get('kgi_time') == None :
            r.set('kgi_time',0)
        else :
            pass
        return float(r.get('kgi_time'))
    
    def time_to_seconds_kgi(self,input):
        ts = input.split(" ")
        if len(ts) == 5:
            datetime_datetime = datetime.datetime.strptime(ts[2]+"-"+ts[1]+"-"+ts[0]+"-"+ts[3],"%Y-%b-%d-%X")
            seconds = time.mktime(datetime_datetime.timetuple())
        else : 
            datetime_datetime = datetime.datetime.strptime(ts[3]+"-"+ts[2]+"-"+ts[1]+"-"+ts[4],"%Y-%b-%d-%X")
            seconds = time.mktime(datetime_datetime.timetuple())
        return seconds