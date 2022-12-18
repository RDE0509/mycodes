# Databricks notebook source
from pyspark.sql import SparkSession


# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------

spark= SparkSession.builder.appName('Spark').getOrCreate()

# COMMAND ----------

data = [
        ('James',['Java','Scala'],{'hair':'black','eye':'brown'}),
        ('Michael',['Spark','Java',None],{'hair':'brown','eye':None}),
        ('Robert',['CSharp',''],{'hair':'red','eye':''}),
        ('Washington',None,None),
        ('Jefferson',['1','2'],{})]

# COMMAND ----------

df = spark.createDataFrame(data=data, schema = ['name','knownLanguages','properties'])

# COMMAND ----------

df.show()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.select(df.name,explode(df.knownLanguages)).show()

# COMMAND ----------

df.select(df.name,explode_outer(df.knownLanguages)).show()

# COMMAND ----------

df.select(df.name,posexplode(df.knownLanguages)).show()

# COMMAND ----------

df.select(df.name,posexplode_outer(df.knownLanguages)).show()

# COMMAND ----------

data1 = [("Banana",1000,"USA"), ("Carrots",1500,"USA"), ("Beans",1600,"USA"), \
      ("Orange",2000,"USA"),("Orange",2000,"USA"),("Banana",400,"China"), \
      ("Carrots",1200,"China"),("Beans",1500,"China"),("Orange",4000,"China"), \
      ("Banana",2000,"Canada"),("Carrots",2000,"Canada"),("Beans",2000,"Mexico")]

# COMMAND ----------

columns1= ["Product","Amount","Country"]

# COMMAND ----------

df1 = spark.createDataFrame(data = data1, schema = columns1)

# COMMAND ----------

df1.show()

# COMMAND ----------

pivotDF = df1.groupBy("Product").pivot("Country").sum("Amount")

# COMMAND ----------

pivotDF.show()

# COMMAND ----------

unpivotExpr = "stack(3, 'Canada', Canada, 'China', China, 'Mexico', Mexico) as (Country,Total)"
unPivotDF = pivotDF.select("Product", expr(unpivotExpr)) \
    .where("Total is not null")

# COMMAND ----------

unPivotDf.show()
