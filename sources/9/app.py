import json
import os
import smtplib
from email.mime.text import MIMEText

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

# Company Info
INFO = {
    "question_tel": "02-1234-5678",
    "question_address": "서울시 강남구",
    "question_email": "godmoon00@gmail.com",
    "question_worktime": "9AM to 6PM"
}

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
    action = req.get("result").get("action")
    if action == "report":
        parameters = req.get("result").get("parameters")
        user_email = parameters.get("email")
        report_type = parameters.get("report_type")
        report_content = parameters.get("report_content")
        mail_content = "{0}\n내용: {1}\n보낸이: {2}".format(report_type, report_content, user_email)

        # email
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()  # say Hello
        smtp.starttls()  # TLS 사용시 필요
        smtp.login('godmoon00@gmail.com', 'dlaansgur77!!')

        msg = MIMEText(mail_content)
        msg['Subject'] = '새로운 문의'
        msg['To'] = 'godmoon00@gmail.com'
        smtp.sendmail('godmoon00@gmail.com', 'godmoon00@gmail.com', msg.as_string())

        smtp.quit()

        text = "소중한 의견 감사합니다. 24시간 내에 답변드리도록 하겠습니다."
        return makeReturn(text, "webhook-report")

    elif action == "question":
        parameters = req.get("result").get("parameters")
        map = {"question_worktime": "근무시간", "question_address": "주소", "question_tel": "전화번호", "question_email": "이메일"}
        question = getQuestion(parameters)

        text = "저희 회사의 {0}는 {1}입니다.".format(map[question], INFO[question])
        return makeReturn(text, "webhook-question")


def getQuestion(parameters):
    for i, j in parameters.items():
        if j is not "":
            return i

    return ""


def makeReturn(text, source):
    return {
        "speech": text,
        "displayText": text,
        "source": source
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, port=port, host='0.0.0.0')
