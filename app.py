from flask import Flask, request, jsonify
from ultrabot import ultraChatBot
import json
from pymongo import MongoClient
from urlextract import URLExtract



app = Flask(__name__)


client = MongoClient('mongodb+srv://rahuranjan3455:WuyQ95xxOWMyArfB@cluster0.yjbj6ol.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client.get_database('subdomain')
collection = db.get_collection('hdfc')

if client is not None:
    print("Connected to MongoDB")

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = ultraChatBot(request.json)
        return bot.Processingـincomingـmessages()
    
@app.route('/get', methods=['GET'])
def hi():
    if request.method == 'GET':
        data = collection.find()
        data = list(data)
        for i in data:
            i.pop('_id')
            print(i)
        return jsonify(data)



@app.route("/getURL", methods=['GET'])
def getURL():
    if request.method == 'GET':
        text = "Hi 968675xxxx, Your Loan Amount of Rs.983200/- has been Successfully Disbursed to Your Account. Withdraw Now 7ko4.com/vtgvro90m06mp either you can visit 1paytag.hdfcbank.com"
        extractor = URLExtract()
        urls = extractor.find_urls(text)
        print(urls)
        # Query MongoDB collection for matching subdomains
        matching_subdomains = collection.find({"subdomain": {"$in": urls}}, {"_id": 0, "subdomain": 1})

        # Extract subdomains from matching documents
        matched_subdomains = [doc["subdomain"] for doc in matching_subdomains]

        return jsonify(matched_subdomains)



if(__name__) == '__main__':
    app.run(debug=True, port=5001)

