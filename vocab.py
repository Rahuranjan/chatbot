
from flask import Flask, Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"

@auth.route('/bye')
def bye():
    return "Goodbye, World!"
