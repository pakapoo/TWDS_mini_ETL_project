from pyspark.sql import SparkSession

def readcsv(folderPath):
    spark = SparkSession \
            .builder \
            .config("spark.driver.extraClassPath", "/Users/mark/Desktop/job/take home project/TWDS_mini_ETL_project/spark/jars/mysql-connector-j-8.3.0.jar") \
            .getOrCreate()
    return spark.read.csv(folderPath, 
                          inferSchema=True, 
                          header=True)