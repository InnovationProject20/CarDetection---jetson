#!/bin/sh
redis-cli -a project123 FLUSHDB
python3 jetsonRedisRetrieval.py $1
