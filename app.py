from flask import Flask, Response, request, jsonify, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import pandas as pd


app = Flask(__name__)

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



# ========================================================

# Fetches budgetid & saleid Then increment them by 1
def getid(x):
    # x -> str
    idData=0
    fetchDoc = collectionIdentity.find_one({"id": 1})
    if x=="b":
        idtype = "budgetid"
    elif x=="s":
        idtype = "saleid"
    idData = fetchDoc[idtype]
    collectionIdentity.update_one({"id": 1},{"$inc":{idtype:1}})
    return idData



@app.route("/")
def home():
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



@app.route('/uploadf', methods=['GET','POST'])
def read_excel_rows():
    if 'file' not in request.files:
        return render_template('index.html')
    excel_file = request.files['file']
    if excel_file.filename == '':
        return jsonify({'error': 'No selected file'})

    df = pd.read_excel(excel_file, header=1)
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
    return Response("Data uploaded successfully")




if __name__== '__main__':
    app.run(debug=True)
