from flask import Flask
from flask import request
from flask import Response
import json
from flask import make_response
from flask import render_template
import uuid
import datetime
app = Flask(__name__)

@app.route("/serve")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)


@app.route("/", methods=["POST"])
def result():
	resp = make_response()

	#check if new visitor :
	if 'ss_s' not in  request.cookies:
		print "sa"
		user_id = uuid.uuid4()
		expire_date = datetime.datetime.now()
		expire_date = expire_date + datetime.timedelta(days=360)
		resp.set_cookie("ss_s",user_id,expires=expire_date)

	if 'ss_u' not in request.cookies:
		user_id = uuid.uuid4()
		expire_date = datetime.datetime.now()
		expire_date = expire_date + datetime.timedelta(days=1)
		resp.set_cookie("ss_u",user_id,expires=expire_date)

	if 'ss_a' not in request.cookies:
		user_id = uuid.uuid4()
		expire_date = datetime.datetime.now()
		expire_date = expire_date + datetime.timedelta(minutes=15)
		resp.set_cookie("ss_a",user_id,expires=expire_date)
		
	if '__is_stream' not in request.cookies:
		user_id = uuid.uuid4()
		expire_date = datetime.datetime.now()
		expire_date = expire_date + datetime.timedelta(minutes=15)
		resp.set_cookie("ss_a",user_id,expires=expire_date)

	#print type(request.cookies)
	#return str(request.cookies)

	#resp.set_cookie("deneme12")
	#result = request.data
	#body_data = json.loads(result)
	#print body_data

	resp.headers["Access-Control-Allow-Origin"]='*'
	return resp


if __name__ == '__main__':
    app.run(port=5000,debug=True,host="localhost")
