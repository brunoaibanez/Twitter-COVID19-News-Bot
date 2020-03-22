
import findspark
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql.functions import desc
import time
from collections import namedtuple
import json

with open('properties_user', 'r') as f:
 user_data = json.load(f)


def run_spark():
    findspark.init(user_data['findspark_path'])
    # Can only run this once. restart your kernel for any errors.
    sc = SparkContext()

    ssc = StreamingContext(sc, 10)

    socket_stream = ssc.socketTextStream(user_data['host'], user_data['port'])

    lines = socket_stream.window(20)

    fields = ("tag", "count")
    Tweet = namedtuple('Tweet', fields)

    # Use Parenthesis for multiple lines or use \.
    (lines.flatMap(lambda text: text.split(" "))  # Splits to a list
     .filter(lambda word: word.lower().startswith("#"))  # Checks for hashtag calls
     .map(lambda word: (word.lower(), 1))  # Lower cases the word
     .reduceByKey(lambda a, b: a + b)  # Reduces
     .map(lambda rec: Tweet(rec[0], rec[1]))  # Stores in a Tweet Object
     .foreachRDD(lambda rdd: rdd.toDF().sort(desc("count"))  # Sorts Them in a DF
                 .limit(10).registerTempTable("tweets")))  # Registers to a table.

    ssc.start()
    while True:
      time.sleep(0.1)

# ssc.stop()


if __name__ == "__main__":
    run_spark()