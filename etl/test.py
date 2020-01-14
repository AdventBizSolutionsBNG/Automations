from pyspark.sql import SparkSession
from pyspark import SparkContext
import pandas as pd
from datetime import datetime

# sc = SparkContext()
  
# rdd = sc.parallelize([("a", 1)])
# print(hasattr(rdd, "toDF"))

# spark = SparkSession(sc)
# print(hasattr(rdd, "toDF"))

# df=[]

# rraw = sc.textFile("C:\\Mywork\\Advent\\ETL\\data\\DEMO1\\DEMO1-ORG1\\DEMO1-ORG1-0001\\DEMO1-ORG1-0001-0001\\Invoices\invoices.txt").zipWithIndex().filter(lambda x: x[1] >=2).filter(lambda y: y[1] <=10)
# r1 = rraw.map(lambda x:  (x[1], "ST001","DMOR01", "ORG001-ENT01","ACTRBL", x[0].split("\t")))
# df[0] = r1.toDF()
# df[0].show()

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

sfile = "invoices"
starget = str(datetime.now().strftime("%Y%m%d-%H.%M.%S"))
print(starget)