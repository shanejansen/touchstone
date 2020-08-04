from pyspark.sql import SparkSession

from config import Config

config = Config()
spark = SparkSession.builder.appName('app').getOrCreate()

emails = spark.read.csv('./touchstone/io/emails.csv').toDF('name', 'email')
numbers = spark.read.format('jdbc').options(
    url=f'jdbc:mysql://{config.vars["db_host"]}:{config.vars["db_port"]}/myapp',
    driver='com.mysql.jdbc.Driver',
    dbtable='numbers',
    user=config.vars['db_username'],
    password=config.vars['db_password']
).load().toDF('name', 'number')

people = emails.join(numbers, ['name'])
people.show()
people \
    .coalesce(1) \
    .write \
    .mode('overwrite') \
    .csv('./touchstone/io/output')
