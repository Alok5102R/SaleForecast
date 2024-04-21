import time
from celery import Celery
from celery.utils.log import get_task_logger
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import pandas as pd
import openpyxl

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

load_dotenv()


# ========================================================
# MongoDB configuration

mongodbString=os.getenv("mongodb")
client = MongoClient(mongodbString)
db = client['SalesForecast']                                                             # MongoDB database
collectionBudget = db['BudgetData']                                                      # MongoDB collection
collectionSale = db['SaleData']                                                          # MongoDB collection
collectionIdentity = db['IdentityData']                                                  # MongoDB collection
collectionFile = db['testfile']                                                          # MongoDB collection


@app.task()
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y

@app.task
def generateFileData():
    logger.info('Got Request - Starting work ')
    dataid = collectionIdentity.find_one({"id": 1})
    budgetid = dataid["budgetid"]
    saleid = dataid["saleid"]
    articleList = []
    weekNoList = []
    quantityList = []
    for i in range(1, saleid):
        saledata = collectionSale.find_one({"id": i})
        for j in range(2, budgetid):
            budgetDataPrevious = collectionBudget.find_one({"id": j-1})
            budgetDataCurrent = collectionBudget.find_one({"id": j})
            quantity = saledata["avgsales"] * 7 * (budgetDataCurrent["budget"]/budgetDataPrevious["budget"])
            articleList.append(saledata["article"])
            weekNoList.append(budgetDataCurrent["week"])
            quantityList.append(round(quantity,2))
    forecastData = {
        "Article" : articleList,
        "WeekNo" : weekNoList,
        "Quantity" : quantityList
        }
    
    return forecastData