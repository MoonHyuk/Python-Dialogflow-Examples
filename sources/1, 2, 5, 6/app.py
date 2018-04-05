import os
import json
import urllib.parse
import urllib.request

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
    client_id = "EVaPCD4GueZdSwk5ZoWX"
    client_secret = "S_Kd4wliJ5"
    encText = urllib.parse.quote(req.get("result").get("resolvedQuery"))
    data = None

    action = req.get("result").get("action")
    if action == "translate":
        encText = urllib.parse.quote(req.get("result").get("parameters").get("text"))
        to_language = req.get("result").get("parameters").get("country")
        if to_language == "영어": to_language = "en"
        elif to_language == "중국어": to_language = "zh-CN"
        else: to_language = "es"
        url = "https://openapi.naver.com/v1/papago/n2mt"
        data = "source=ko&target={0}&text={1}".format(to_language, encText)

    elif action == "typo":
        url = "https://openapi.naver.com/v1/search/errata.json?query={0}".format(encText)

    elif action == "dictionary":
        url = "https://openapi.naver.com/v1/search/encyc.json?query={0}".format(encText)

    elif action == "local":
        url = "https://openapi.naver.com/v1/search/local.json?query={0}".format(encText)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    if data is not None:
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    else:
        response = urllib.request.urlopen(request)

    rescode = response.getcode()

    if (rescode == 200):
        response_body = response.read()

        response_json = json.loads(response_body.decode('utf-8'))

        print(response_json)
        if action == "translate":
            result = response_json.get("message").get("result").get("translatedText")

        elif action == "typo":
            result = response_json.get("errata")

        elif action == "dictionary":
            result = response_json.get("items")[0].get("description")

        elif action == "local":
            items = response_json.get("items")
            result = ""
            i = 1
            for item in items:
                result += "{0}. {1}\n위치: {2}\n전화번호: {3}\n\n".format(str(i), item.get("title"), item.get("roadAddress"), item.get("telephone"))
                i+=1
                if i > 5: break

        print(result)
        return {
            "speech": result,
            "displayText": result,
        }
    else:
        print("Error Code:" + rescode)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
