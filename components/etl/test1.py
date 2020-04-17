from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, HiveContext,SQLContext
import pandas as pd
from datetime import datetime
from pyspark.sql.functions import *
from datetime import datetime
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DateType
 
#SparkContext.setSystemProperty("hive.metastore.uris", "thrift://localhost:9083")
import pyhs2
#username="setupadmin", password="admin@1234",
from pyhive import hive
#cursor = hive.connect(host='127.0.0.1', port=10001, auth="NONE",  database='st001_org001_actrbl').cursor()
#cursor.execute('SELECT count(*) from st001_org001_actrbl.ACTRBL_KPI_001_CMPNT_002_HIST')
#print (cursor.fetchall())
#print("done!!!")

 
confCxt = SparkConf() \
            .setAppName("App1") \
            .setMaster("local") \
            .set("spark.sql.warehouse.dir" ,"/user/hive/warehouse") \
            .set("hive.metastore.uris", "thrift://localhost:9083") \
            .set("spark.hadoop.dfs.client.use.datanode.hostname", "true") \
            .set("hive.exec.dynamic.partition.mode" , "nonstrict")
# #sc = SparkContext(conf = confCxt)
# #hv = HiveContext(sc)
# #hv.setConf("hive.metastore.uris", "thrift://192.168.0.7:9083")
mySpark = SparkSession.builder.config(conf=confCxt).config("hive.metastore.uris", "thrift://127.0.0.1:9083").config("hive.exec.dynamic.partition.mode", "nonstrict").config("hive.exec.dynamic.partition" , "true").enableHiveSupport().getOrCreate()

# df = mySpark.sql("select * from st001_org001_actrbl.ACTRBL_KPI_001_CMPNT_002")
# df.show()
# #sc = SparkContext(conf = confCxt).getOrCreate
# #sc = mySpark.sparkContext
#sqlContext = SQLContext(sc)

#SparkContext.setSystemProperty("hive.metastore.uris", "thrift://192.168.0.7:9083")

# confCxt.set("spark.dynamicAllocation.enabled", "true")
# confCxt.set("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true")             
# spark = SparkSession.builder.config(conf=confCxt).enableHiveSupport().getOrCreate()
#spark.sql("create database test")
 
#mySpark.sql("create database st001_org001_actrbl")

#df = mySpark.read.csv("/home/setupadmin/adbiz/components/etl/input/actrbl/invoices/customer.txt",sep=",", header = True, inferSchema= True, mode = "DROPMALFORMED")
# df = mySpark.sql("select * from  ST001_ORG001_ACTRBL.CNT_ACTRBL_INVOICE_005_ext")
# df.show()
# print("Saving as Hive table..")
# df.write.mode("append").saveAsTable("st001_org001_actrbl.sample_ext_parquet_3") 
# df.show()
# print("Saving a Parquet file...")
# df.write.option("compression","snappy").parquet("/home/setupadmin/adbiz/components/etl/output/sample_ext_partition_3.parquets", mode = 'append')


#print("Creating a hive table on Parquet files..")
#sTarget = "/home/setupadmin/adbiz/components/etl/output/actrbl/aggregates/AGG_ACTRBL_INVOICE_002"
# # df = mySpark.read.parquet(sTarget) \
# #     .filter(col("siteCode") == sSiteCode) \
# #     .filter(col("organizationCode") == sOrgCode) \
# #     .filter(col("moduleCode") == sModCode) \
# #     .filter(col("objCode") == sObjCode) \
# #     .filter(col("containerCode") == sContainerCode) \
# #     .filter(col("aggCode") == sAggCode) \
# #     .filter(col(sFilterAttributeYear) >= iYear) \
# #     .filter(col(sFilterAttributeMonth) >= iMonth)    \
# #     .filter(col(sFilterAttributeDay) >= iDay)
#df = mySpark.read.load("/home/setupadmin/adbiz/components/etl/output/actrbl/containers/CNT_ACTRBL_INVOICE_005/")
# df = mySpark.read.load(sTarget)
df.show()
# #df = mySpark.read.csv("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\ST001\\ORG001\\ENT001\\ACTRBL\\input\\Invoices\\2018\\sample1.txt",sep=",", header = True, inferSchema =  True, mode = "DROPMALFORMED")
# cols = df.dtypes
# buf = []
# buf.append('CREATE EXTERNAL TABLE IF NOT EXISTS st001_org001_actrbl.sample_ext_parquet_4 (')
# keyanddatatypes =  df.dtypes
# sizeof = len(df.dtypes)
# print ("size----------",sizeof)
# count=1
# for eachvalue in keyanddatatypes:
#     print (count,sizeof,eachvalue)
#     if count == sizeof:
#         total = str(eachvalue[0])+str(' ')+str(eachvalue[1])
#     else:
#         total = str(eachvalue[0]) + str(' ') + str(eachvalue[1]) + str(',')
#     buf.append(total)
#     count = count + 1

# buf.append(' )')
# buf.append(' STORED as parquet ')
# buf.append("LOCATION")
# buf.append("'")
# buf.append('/home/setupadmin/adbiz/components/etl/output/sample_ext_partition_3.parquets')
# #buf.append(sTarget)
# buf.append("'")
# #buf.append("'")
# ##partition by pt
# tabledef = ''.join(buf)

# # # print ("---------print definition ---------")
# print(tabledef)
# # ## create a table using spark.sql. Assuming you are using spark 2.1+
# # #tabledef = "CREATE EXTERNAL TABLE IF NOT EXISTS st001_org001_actrbl.sample_ext_partition (siteCode string,organizationCode string,entityCode string,moduleCode string,YEAR int,QUARTER int,MONTH int,DAY int,ShipSite string,ShipSiteName string,InvoiceNumber string,InvoiceDate string,SalesOrder string,SODate string,GSTNo string,Channel string,CustomerCode string,CustomerName string,City string,State string,Country string,CustomerType string,Category string,CustomerRegion string,ProductLine string,Description string,Sequence int,ProductCode string,Desc1 string,Desc2 string,InvoiceQty int,UnitPrice int,ListPrice int,PriceListMasterAvailable string,DiscountPercent string,DiscountValue int,TotalDiscountPercent string,TotalDiscountValue int,InvoiceValue int,InvoiceValueINR int,Currency string,Currency1 string,Currency2 string,Rate1 int,Rate2 int,BOL string,PaymentTerms string,PaymentDescription string,Taxusage string,TaxEnv string,Taxclass string,SalesCGST string,SalesCGSTValue int,SalesHandlingCharges string,SalesHandlingChargesValue string,SalesIGST string,SalesIGSTValue string,SalesPackingForward string,SalesPackingForwardValue int,SalesSGST string,SalesSGSTValue int,TCSGST string,TCSGSTValue string,LineAmount int,Assessablevalue int,CustomerPart string,CancelledInvoiceNo string,IsInvoiceCancelled string,CustomerPO string,InvoiceYear int,InvoiceMonth int,PriceDiff int,PerUnitPrice int,PerUnitListPrice int ) STORED as parquet LOCATION'/home/setupadmin/adbiz/components/etl/output/sample_ext_partition.parquets'"
# # #tabledef = "CREATE EXTERNAL TABLE IF NOT EXISTS st001_org001_actrbl.sample_ext_partition (YEAR int,QUARTER int,MONTH int,DAY int,ShipSite string,ShipSiteName string,InvoiceNumber string,InvoiceDate string,SalesOrder string,SODate string,GSTNo string,Channel string,CustomerCode string,CustomerName string,City string,State string,Country string,CustomerType string,Category string,CustomerRegion string,ProductLine string,Description string,Sequence int,ProductCode string,Desc1 string,Desc2 string,InvoiceQty int,UnitPrice int,ListPrice int,PriceListMasterAvailable string,DiscountPercent string,DiscountValue int,TotalDiscountPercent string,TotalDiscountValue int,InvoiceValue int,InvoiceValueINR int,Currency string,Currency1 string,Currency2 string,Rate1 int,Rate2 int,BOL string,PaymentTerms string,PaymentDescription string,Taxusage string,TaxEnv string,Taxclass string,SalesCGST string,SalesCGSTValue int,SalesHandlingCharges string,SalesHandlingChargesValue string,SalesIGST string,SalesIGSTValue string,SalesPackingForward string,SalesPackingForwardValue int,SalesSGST string,SalesSGSTValue int,TCSGST string,TCSGSTValue string,LineAmount int,Assessablevalue int,CustomerPart string,CancelledInvoiceNo string,IsInvoiceCancelled string,CustomerPO string,InvoiceYear int,InvoiceMonth int,PriceDiff int,PerUnitPrice int,PerUnitListPrice int ) PARTITIONED BY (siteCode string,organizationCode string,entityCode string,moduleCode string) STORED as parquet LOCATION'/home/setupadmin/adbiz/components/etl/output/sample_ext_partition.parquets'"
# mySpark.sql(tabledef)
# newDF = mySpark.sql("select * from st001_org001_actrbl.sample_ext_partition_3")
# print(newDF.show())

#newDF = mySpark.sql("select * from st001_org001_actrbl.sample_ext_partition_2")
#print(newDF.show())

#df.write.mode("append").saveAsTable("invoice_temp")
#df.createOrReplaceTempView("invoice_temp")
# df.createGlobalTempView("invoices")
# mySpark.sql("select * from global_temp.invoices").show()
# mySpark.newSession().sql("select * from global_temp.invoices")
# mySpark.sql("select * from invoice_temp")

# df.write.mode("append").saveAsTable("invoice_temp")

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
 
