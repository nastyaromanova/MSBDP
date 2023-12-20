import pyspark 
from pyspark.sql import SparkSession

session = SparkSession.builder.master("local").appName("lab5").getOrCreate()
df=session.read.csv("hdfs://haddop1:9000/user/hadoop/mapreduce_base_input/dataset.csv")
df.show(10)
df.write.json("hdfs://haddop1:9000/user/hadoop/mapreduce_base_output/dataset_formatted.json")