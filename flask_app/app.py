from flask import Flask, Response, request, jsonify, render_template, send_file, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import pandas as pd
from celery import Celery
import openpyxl
import time
import io

app = Flask(__name__)
celeryApp = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

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


@app.route('/taskStatus/<task_id>')
def get_status(task_id):
    status = celeryApp.AsyncResult(task_id, app=celeryApp)
    if str(status.state) == "PENDING":
        page = f"""<html>
        <body style="background-color: black;" cz-shortcut-listen="true">
        <h3 align="center" style="color: white;margin-top: 30px;"> We are processing your Request ... </h3> <br> 
        <button type="button" style="background-color: #555599;color:white;padding:5px; border: none; margin-left: 45.5%;"><a href="/taskStatus/{task_id}" style="text-decoration: none; color: white;">Recheck Status</a></button>
        <button type="button" style="background-color: #555599;color:white;padding:5px;border: none;margin-left: 10px;"><a href="/" style="text-decoration: none;color: white;">Home</a></button>
        </body></html>"""
    else:
        page = f"""<html>
        <body style="background-color: black;" cz-shortcut-listen="true">
        <h3 align="center" style="color: white;margin-top: 30px;"> Your Request has been processed. </h3> <br> 
        <button type="button" style="background-color: #555599;color:white;padding:5px; border: none; margin-left: 45.5%;"><a href="/taskFile/{task_id}" style="text-decoration: none; color: white;">Download File</a></button>
        <button type="button" style="background-color: #555599;color:white;padding:5px;border: none;margin-left: 10px;"><a href="/" style="text-decoration: none;color: white;">Home</a></button>
        </body></html>"""
    return Response(page, status=200, content_type='text/html')



def getid(x):
    # x -> str
    idData=0
    fetchDoc = collectionIdentity.find_one({"id": 1})
    if x=="b":
        idType = "budgetid"
    elif x=="s":
        idType = "saleid"
    idData = fetchDoc[idType]
    collectionIdentity.update_one({"id": 1},{"$inc":{idType:1}})
    return idData



@app.route("/home")
def home():
    i=5
    for i in range(5, -1, -1):
        print(i)
    return Response("<h1>Automated Sales Forecast Generator</h1>", status=200)



# Single row addition
@app.route('/upload', methods=['POST','GET'])
def uploadData():
    try:
        if request.form:
            data = request.form.to_dict()
        elif request.json:
            data = request.json
        else:
            return jsonify({'error': 'No data found'})
        postData = {"id":getid("b"), "week":int(data.get('week')), "year":int(data.get('year')), "budget":int(data.get('budget'))}                             # Data Format
    except Exception as e:
        return Response("Error Occured: "+str(e), status=400, mimetype='application/json')
    
    try:
        collectionBudget.insert_one(postData)
    except Exception as e:
        return Response("Error Occured: "+str(e), status=400, mimetype='application/json')
    return Response("Data updated successfully: "+str(data), status=200, mimetype='application/json')



# Single row fetch
@app.route('/fetch', methods=['GET'])
def fetchData():
    try:
        id = int(request.args.get('id'))
        data = collectionBudget.find_one({"id": id})
    except Exception as e:
        return Response("Error Occured: "+str(e), status=400, mimetype='application/json')
    return Response(str(data), status=200)



@app.route('/', methods=['GET','POST'])
def readFileData():
    if 'file' not in request.files:
        return render_template('index.html')
    excel_file = request.files['file']
    if excel_file.filename == '':
        return jsonify({'error': 'No selected file'})

    df = pd.read_excel(excel_file, header=1)                              # header refer to rows which starts from 0
    expected_columns = ["Week", "Year", "Budget", "Article", "AvgSales"]
    df = df[expected_columns]
    rows_data = df.to_dict(orient='records')
    
    listBudgetData = []
    listSaleData = []
    dataid = collectionIdentity.find_one({"id": 1})
    budgetid = dataid["budgetid"]
    saleid = dataid["saleid"]
    for row in rows_data:
        listBudgetData.append({"id":budgetid, "week":int(row['Week']), "year":int(row['Year']), "budget":int(row['Budget'])})                             # Data Format
        budgetid += 1
        if str(row['Article']) != "nan":
            listSaleData.append({"id":saleid, "article":row['Article'], "avgsales":float(row['AvgSales'])})                            # Data Format
            saleid += 1
    collectionBudget.insert_many(listBudgetData)
    collectionSale.insert_many(listSaleData)
    collectionIdentity.update_one({"id": 1},{"$set":{"budgetid":budgetid, "saleid":saleid}})

    page = f"""<html>
        <body style="background-color: black;" cz-shortcut-listen="true">
        <h3 align="center" style="color: white;margin-top: 30px;"> Data uploaded Successfully. </h3> <br> 
        <button type="button" style="background-color: #555599;color:white;padding:5px; border: none; margin-left: 45.5%;"><a href="/" style="text-decoration: none; color: white;">Home</a></button>
        </body></html>"""

    return Response(page, status=200, content_type='text/html')



# It'll provide task id for the Report generation task
@app.route('/downloadf')
def writeFileData():
    app.logger.info("Invoking Method ")
    r = celeryApp.send_task('tasks.generateFileData')
    app.logger.info(r.backend)
    url = f"taskStatus/{str(r.id)}"
    return redirect(url)


# Paste task id in this url and refresh to get the file (file will be saved in flask_app directory, inside docker)
@app.route('/taskFile/<task_id>')
def getFile(task_id):
    status = celeryApp.AsyncResult(task_id, app=celeryApp)
    if(str(status.state)=="SUCCESS"):
        result = celeryApp.AsyncResult(task_id, app=celeryApp).result
        df = pd.DataFrame(result)

        # reportFile = "SalesForecast.xlsx"
        # df.to_excel(reportFile, index=False)
        statusdata = {'status': 'success'}

        # Write the DataFrame to a BytesIO object as an Excel file
        excel_bytes = io.BytesIO()
        df.to_excel(excel_bytes, index=False)

        # Set the BytesIO object's cursor position to the beginning
        excel_bytes.seek(0)

        # Send the BytesIO object as a file attachment in the HTTP response
        fileData =  send_file(
            excel_bytes,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Forecastdata.xlsx'
        )
        return fileData
    else:
        statusdata = "Processing ..."

    return statusdata

