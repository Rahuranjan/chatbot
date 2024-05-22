from flask import Flask, request, jsonify
from ultrabot import ultraChatBot
import json
from pymongo import MongoClient
from urlextract import URLExtract
from twilio.twiml.messaging_response import MessagingResponse
import requests
from vocab import auth
from whatsappBot import create_app
import logging



# app = Flask(__name__)
app = create_app()

client = MongoClient('mongodb+srv://rahuranjan3455:WuyQ95xxOWMyArfB@cluster0.yjbj6ol.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = client.get_database('subdomain')
collection = db.get_collection('hdfc')

if client is not None:
    print("Connected to MongoDB")


app.register_blueprint(auth)


# @app.route('/', methods=['POST'])
# def home():
#     if request.method == 'POST':
#         bot = ultraChatBot(request.json)
#         return bot.Processingـincomingـmessages()
    
# @app.route('/get', methods=['GET'])
# def hi():
#     if request.method == 'GET':
#         data = collection.find()
#         data = list(data)
#         for i in data:
#             i.pop('_id')
#         return jsonify(data)



# @app.route("/getURL", methods=['GET'])
# def getURL():
#     if request.method == 'GET':
#         text = "Hi 968675xxxx, Your Loan Amount of Rs.983200/- has been Successfully Disbursed to Your Account. Withdraw Now 7ko4.com/vtgvro90m06mp either you can visit 1paytag.hdfcbank.com"
#         extractor = URLExtract()
#         urls = extractor.find_urls(text)
#         print(urls)
#         # Query MongoDB collection for matching subdomains
#         matching_subdomains = collection.find({"subdomain": {"$in": urls}}, {"_id": 0, "subdomain": 1})

#         # Extract subdomains from matching documents
#         matched_subdomains = [doc["subdomain"] for doc in matching_subdomains]

#         return jsonify(matched_subdomains)


# @app.route('/vocabulary', methods=['POST'])
# def vocabulary():
#     """
#     WhatsApp Twilio Webhook
#     :return: string response for whatsapp
#     """
#     word_synonym = ""
#     word_antonym = ""
#     incoming_msg = request.values.get('Body', '').lower()
#     resp = MessagingResponse()
#     message = resp.message()
#     responded = False
#     words = incoming_msg.split('-')
#     if len(words) == 1 and incoming_msg == "help":
#         help_string = create_help_message()
#         message.body(help_string)
#         responded = True
#     elif len(words) == 2:
#         search_type = words[0].strip()
#         input_string = words[1].strip().split()
#         if len(input_string) == 1:
#             response = get_dictionary_response(input_string[0])
#             if search_type == "meaning":
#                 message.body(response["meaning"])
#                 responded = True
#             if search_type == "synonyms":
#                 for synonym in response["synonyms"]:
#                     word_synonym += synonym + "\n"
#                 message.body(word_synonym)
#                 responded = True
#             if search_type == "antonyms":
#                 for antonym in response["antonyms"]:
#                     word_antonym += antonym + "\n"
#                 message.body(word_antonym)
#                 responded = True
#             if search_type == "examples":
#                 message.body(response["examples"])
#                 responded = True
#     if not responded:
#         message.body('Incorrect request format. Please enter --help to see the correct format.')
#     return str(resp)



def create_help_message():
    """
    Returns help message for using VocabBot
    :return: string
    """
    help_message = "Improve your vocabulary using *VocabBot*! \n\n" \
        "You can ask the bot the below listed things:  \n"\
        "*meaning* - type the word \n"\
        "*examples* - type the word \n"\
        "*synonyms* - type the word \n"\
        "*antonyms* - type the word \n"
    return help_message


def get_dictionary_response(word):
    """
    Query Webster's Thesaurus API
    :param word: query's word
    :return: definitions, examples, antonyms, synonyms
    """
    word_metadata = {}
    definition = "sorry, no definition is available."
    example = "sorry, no example is available."
    synonyms = ["sorry, no synonyms are available."]
    antonyms = ["sorry, no antonyms are available."]
    api_key = "a5c97867-dac3-49da-86cc-a7790cf53f4a"
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={api_key}"
    
    response = requests.get(url)
    print(response.text)
    api_response = json.loads(response.text)
    if response.status_code == 200:
        for data in api_response:
            try:
                if data["meta"]["id"] == word:
                    try:
                        if len(data["meta"]["sync"]!=0):
                            synonyms = data["meta"]["syns"][0]
                        if len(data["meta"]["ants"]!=0):
                            antonyms = data["meta"]["ants"][0]
                        for results in data["def"][0]["sseq"][0][0][1]["dt"]:
                            if results[0] == "text":
                                definition = results[1]
                            if results[0] == "vis":
                                example = results[1][0]["t"].replace("{it}", "*").replace("{/it}", "*")

                    except KeyError as e:
                        print(e)

            except TypeError as e:
                print(e)
            break
    word_metadata["meaning"] = definition
    word_metadata["examples"] = example
    word_metadata["synonyms"] = synonyms
    word_metadata["antonyms"] = antonyms

    return word_metadata


if(__name__) == '__main__':
    logging.info("Flask app is running.")
    app.run(debug=True, port=5001)

