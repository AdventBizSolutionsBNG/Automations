#from pymongo import MongoClient
import os,sys,traceback
import json
import numpy as np
#from adbiz.components.etl.coreEngine.setup import ClsEtlSettings
from collections import OrderedDict 
#from coreEngine.commonUtils import substract_lists, unique_list
#from adbiz.components.etl.coreEngine.commonUtils import substract_lists, unique_list
import os,sys,traceback, datetime
import json
from datetime import datetime, date
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import uuid
from pyspark.sql.functions import *
from pyspark.sql.functions import lit, when, col, regexp_extract , udf
from pyspark.sql.functions import year, month, quarter, weekofyear, dayofyear, dayofweek, dayofmonth
from pyspark.sql.types import DateType
from dateutil.relativedelta import relativedelta


def addPaymentTermType(pDFSource, pDictAttributes):
    try:
        dFTemp = pDFSource.withColumn( "paymentTermType", lit("Sample Payterm Type"))
        return dFTemp

    except Exception as e:
        print(e)

def addCancelledInvoiceNumber(pDFSource, pDictAttributes):
    try:
        dFTemp = pDFSource.withColumn( "canceledInvoiceNumber", lit("123232344"))
        return dFTemp

    except Exception as e:
        print(e)

def addPaymentTermDays(pDFSource, pDictAttributes):
    try:
        dFTemp = pDFSource.withColumn( "paymentTermDays", lit("60"))
        return dFTemp

    except Exception as e:
        print(e)

def addInvoiceStatus(pDFSource, pDictAttributes):
    try:
        dFTemp = pDFSource.withColumn( "invoiceStatus", lit("Open"))
        return dFTemp

    except Exception as e:
        print(e)