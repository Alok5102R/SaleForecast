from flask import Flask, Response, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv


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


# ========================================================

def getid(x):
    # x -> str
    if x=="b":
        fetchDoc = collectionIdentity.find_one({"id": 1})
        idData = fetchDoc["budgetid"]
    elif x=="s":
        fetchDoc = collectionIdentity.find_one({"id": 1})
        idData = fetchDoc["saleid"]
    else:
        idData = None
    return idData

def setid(x):
    # x -> str
    if x=="b":
        collectionIdentity.update_one({"id": 1},{"$inc":{"budgetid":1}})
    elif x=="s":
        collectionIdentity.update_one({"id": 1},{"$inc":{"saleid":1}})
    else:
        pass



@app.route("/")
def home():
    return Response("<h1>Automated Sales Forecast Generator</h1>", status=200)



# Single row addition
@app.route('/upload', methods=['POST','GET'])
def upload_data():
    try:
        if request.form:
            data = request.form.to_dict()
        elif request.json:
            data = request.json
        else:
            return jsonify({'error': 'No data found'})
        postData = {"id":getid("b"), "week":int(data.get('week')), "year":int(data.get('year')), "budget":int(data.get('budget'))}                             # Data Format
        setid("b")
    except Exception as e:
        return Response("Error Occured: "+str(e), status=400, mimetype='application/json')
    
    try:
        collectionBudget.insert_one(postData)
    except Exception as e:
        return Response("Error Occured: "+str(e), status=400, mimetype='application/json')
    return Response("Data updated successfully: "+str(data), status=200, mimetype='application/json')



# Single row fetch
@app.route('/fetch', methods=['GET'])
def fetch_data():
    try:
        id = int(request.args.get('id'))
        data = collectionBudget.find_one({"id": id})
    except Exception as e:
        return Response("Error Occured: "+str(e), status=400, mimetype='application/json')
    return Response(str(data), status=200)

















if __name__== '__main__':
    app.run(debug=True)
