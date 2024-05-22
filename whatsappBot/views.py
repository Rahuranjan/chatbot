import logging
import json
from flask import Blueprint, request, jsonify, current_app

webhook_blueprint = Blueprint("webhook", __name__)

def handle_message():
    """
    handle incomming webhook events from the ehatsApp API.

    This function processes incomming whatsApp message and other events, 
    such as delivery statuses. if the event is a valid message, it gets 
    processed. if the incomming payload is not a recognized WhatsApp event,
    an error is returned.

    Every message send will trigger 4 HTTP requests to your webhook: message, sent, delivered, read.

    Returns:
        response: A tuple containing a JSON response and an HTTP status code.
    """

    body = request.get_json()
    # logging.info(f"Webhook received: {body}")

    # Check if it's a WHatsApp status update
    if(body.get("entry"),[{}][0].get("changes", [{}][0]).get("value", {}).get("statuses")):
        logging.info("Received a WhatsApp status update.")
        return jsonify({"status": "ok"}), 200
    
    

def verify():
    # Parse params from the webhook verification request
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    # Check if a token and mode were sent
    if mode and token:
        # Check the mode and token sent are correct
        if mode == "subscribe" and token == current_app.config["VERIFY_TOKEN"]:
            # Respond with 200 OK and challenge token from the request
            logging.info("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Responds with '403 Forbidden' if verify tokens do not match
            logging.info("VERIFICATION_FAILED")
            return jsonify({"status": "error", "message": "Verification failed"}), 403
    else:
        # Responds with '400 Bad Request' if verify tokens do not match
        logging.info("MISSING_PARAMETER")
        return jsonify({"status": "error", "message": "Missing parameters"}), 400
    

@webhook_blueprint.route("/webhook", methods=["GET"])
def webhook_get():
    return verify()
    