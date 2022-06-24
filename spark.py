from pyspark.sql import SparkSession

def get_spark_session():
    ''' No parameters, returns spark session object'''
    if get_env() == 'DEV':
        spark = SparkSession.builder.master('local').appName(get_appName()).getOrCreate()
    return spark 
