import os
import json
import random
from datetime import datetime

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)
    res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    random.seed(datetime.now())
    speech = "그리하거라." if random.random() > 0.5 else "그러지 말거라."
    return {
        "speech": speech,
        "displayText": speech,
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
