tar xf redis-stable.tar.gz
~/redis-stable/src/redis-server &
tar xf milvus_1.0.tar.gz
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD/milvus/lib
cd milvus/scripts
sh start_server.sh &
cd ../../
python3 to_redis.py
python3 to_milvus.py
