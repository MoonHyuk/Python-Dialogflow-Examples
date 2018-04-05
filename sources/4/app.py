import os
import json

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
    if req.get("result").get("action") != "sort":
        return {}
    parameters = req.get("result").get("parameters")
    data = [int(i) for _, i in parameters.items() if i is not ""]
    data.sort()
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):
    speech = "정렬 결과는 " + ', '.join(str(i) for i in data) + "입니다."
    return {
        "speech": speech,
        "displayText": speech,
        "source": "apiai-sort-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
