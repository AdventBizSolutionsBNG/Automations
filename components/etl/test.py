from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, HiveContext,SQLContext
import pandas as pd
from datetime import datetime
from pyspark.sql.functions import *
from datetime import datetime
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DateType
 
#SparkContext.setSystemProperty("hive.metastore.uris", "thrift://localhost:9083")

 
confCxt = SparkConf() \
            .setAppName("App1") \
            .setMaster("local") \
            #.set("spark.sql.warehouse.dir" ,"C:\\hadoop\\hive\\spark-warehouse" )

mySpark = SparkSession.builder.config(conf=confCxt).enableHiveSupport().getOrCreate()
#sc = SparkContext(conf = confCxt).getOrCreate
sc = mySpark.sparkContext
sqlContext = SQLContext(sc)

SparkContext.setSystemProperty("hive.metastore.uris", "thrift://localhost:9083")

# confCxt.set("spark.dynamicAllocation.enabled", "true")
# confCxt.set("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true")             
# spark = SparkSession.builder.config(conf=confCxt).enableHiveSupport().getOrCreate()
#spark.sql("create database test")
 
#mySpark.sql("create database st001_org001_actrbl")

df = mySpark.read.csv("/home/setupadmin/adbiz/components/etl/input/actrbl/invoices/sample1.txt", sep = ",", header = True, mode = "DROPMALFORMED")
#df = spark.read.load("C:\Mywork\Advent\ETLFramework\etl\output\containers\siteCode=ST001\organizationCode=ORG001\moduleCode=ACTRBL\objCode=invoice\containerId=CNT_ACTRBL_INVOICE_000")
#print(df.show())

#df.write.mode("append").saveAsTable("invoice_temp")
df.createOrReplaceTempView("invoice_temp")
mySpark.sql("select * from invoice_temp")

df.write.mode("append").saveAsTable("invoice_temp")

#mySql = spark.sql("select * from ST001_ORG001_ACTRBL.invoice")
#print(mySql.show())

# sc = spark.sparkContext
# _ALL_COLUMN_LIST = "shipSite,shipSiteName,invoiceId,invoiceDate,invoiceStatus,invoiceType,invoiceCategory,salesOrderId,salesOrderDate,gstID,channel,customerCode,customerName,city,state,country,customerType,productCategory,customerRegion,productLine,productType,lineItem,productCode,productDescription_1,productDescription_2,invoiceQty,unitPrice,List Price,isPriceListMasterAvailable,discountPercent,discountValue,totalDiscountPercent,totalDiscountValue,invoiceValue,invoiceValueINR,currency,currency1,currency2,rate1,rate2,BOL,paymentTerms,paymentDescription,taxUsage,taxCategory,taxClass,salesCGSTCharges,salesCGSTValue,salesHandlingCharges,salesHandlingChargesValue,salesIGSTCharges,salesIGSTValue,salesPackingForwardCharges,salesPackingForwardValue,salesSGSTCharges,salesSGSTValue,salesTCSGSTCharges,salesTCSGSTValue,totalLineAmount,totalAssessablevalue,customerPartNumber,customerPONumber"
# rdd = sc.parallelize([("a", 1)])
# print(hasattr(rdd, "toDF"))

#spark = SparkSession(sc)
# print(hasattr(rdd, "toDF"))

# df=[]
#df = spark.read.csv("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\output.csv", header = True, mode = "DROPMALFORMED",  )
#print(df.show())

#df.write.partitionBy(["siteCode","organizationCode","moduleCode","objCode", "containerCode", "entityCode", "divCode", "invoiceDate_YEAR","invoiceDate_QUARTER", "invoiceDate_Month","invoiceDate_DAY"]).option("compression","snappy").parquet("C:\Mywork\Advent\ETLFramework\etl\output", mode = 'append')
#dfAgg = df.groupby(["siteCode","organizationCode","moduleCode","objCode", "containerCode", "entityCode", "divCode", "invoiceDate_YEAR","invoiceDate_QUARTER", "invoiceDate_Month","invoiceDate_DAY"])

# dforg = spark.read.load("C:\Mywork\Advent\ETLFramework\etl\output\siteCode=ST001\organizationCode=ORG001\moduleCode=ACTRBL\objCode=invoice\containerId=CNT_ACTRBL_INVOICE_000")

#dforg.show()
#dfKeys = dforg.select("Id")
#func =  udf (lambda x: datetime.strptime(x, '%d-%m-%Y'), DateType())
#dfdatekey  = dforg.select ("invoiceDate", year("invoiceDate").alias("year"), to_date("invoiceDate"), func(col('invoiceDate')))
#dfdatekey.show()

# dfgrp = dforg.groupBy("entityCode","divCode" ,"[invoiceDate.YEAR]","[invoiceDate.QUARTER]", "[invoiceDate.Month]", "channel")
# #dfgrp = dfgrp.withColumn("Id", monotonically_increasing_id())
# df1 = dfgrp.agg( count("channel").alias("count") )
# df1.show()
# sOp = 'max("unitPrice").alias("max")'
# dfagg1 = dfgrp.agg(max("unitPrice").alias("max")).withColumn("Id", monotonically_increasing_id())
# #dfagg1 = dfagg1.withColumn("Id", monotonically_increasing_id())
# sName = "invoice_Date"
# dfagg2 = dfgrp.agg(min("unitPrice").alias(sName + "." + "min")).withColumn("Id", monotonically_increasing_id())
# dfagg2.show()
#df = dforg.join(dfagg,"Id","outer")
# df = dfagg1.join (dfagg2, "Id", "inner")
# df.show()

#sc = SparkContext()
#sqlContext = SQLContext(sc)
#pDF = sqlContext.read.load("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\output.csv", format="csv" ,header = "true", interschema = "true")

# rraw = sc.textFile("C:\\Mywork\\Advent\\ETL\\data\\DEMO1\\DEMO1-ORG1\\DEMO1-ORG1-0001\\DEMO1-ORG1-0001-0001\\Invoices\invoices.txt").zipWithIndex().filter(lambda x: x[1] >=2).filter(lambda y: y[1] <=10)

# r1 = rraw.map(lambda x:  (x[0].split("\t")))
# #myRdd = rddSourceData.map(lambda x: (x[1], x[0]))
# #print(r1.collect())
# df = r1.toDF(_ALL_COLUMN_LIST.split(","))
# print(df.show())

# rdate1 = rraw.map(lambda x: (x[1], x[0].split('\t')[3][6:11] + x[0].split("\t")[3][3:5] + x[0].split("\t")[3][0:2]))
# df1 = rdate1.toDF(["Id", "OrderDate"])
# df1.show()

# rdate2 = rraw.map(lambda x: (x[1], x[0].split('\t')[5][6:11] + x[0].split("\t")[5][3:5] + x[0].split("\t")[5][0:2]))
# df2 = rdate2.toDF(["Id", "InvoiceDate"])
# df2.show()

# dfnew = df1.join(df2,df1.Id == df2.Id).select(df1.Id, df1.OrderDate, df2.InvoiceDate)
# dfnew.show()

# df1.select("OrderDate").show()
# print(df1.select("OrderDate").distinct().count())

#df2.show()
 
