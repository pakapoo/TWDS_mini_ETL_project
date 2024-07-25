from pyspark.sql import SparkSession

def readcsv(folderPath):
    spark = SparkSession.builder.getOrCreate()
    return spark.read.csv(folderPath, inferSchema=True, header=True)