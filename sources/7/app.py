import json
import os
import requests

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
    word = req.get("result").get("parameters").get("word")
    print(word)
    r = requests.post("http://0xF.kr:2580/wordchain/next", data={'char': word})
    next_word = json.loads(r.text).get("data")[0].get("word")
    print(next_word)
    return {
        "speech": next_word,
        "displayText": next_word
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
