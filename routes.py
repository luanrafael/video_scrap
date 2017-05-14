#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Luan Rafael'

from flask import Flask
from flask import Flask, request, redirect

import json
import glob
import os

app = Flask(__name__)


@app.route("/getSpiders/<id>")
@app.route("/getSpiders")
def get_spiders(id = None):

	
	if id is not None:
		json_path = "static/json/" + id
		with open(json_path, 'r') as file:
 			data = json.loads(file.read())
		file.close()
		return json.dumps(data)

	output = []
	json_paths = glob.glob("static/json/*.json")

	
	for json_path in json_paths:
		
		with open(json_path, 'r') as file:
 			data = json.loads(file.read())
		file.close()
		id = json_path.split("/")[-1]
		data['data'] = []
		data['id'] = id
		output.append(data)

	return json.dumps(output)



@app.route("/api/v1/spider/<id>", methods=['POST'])
def update_spider(id):

	data_json = request.json
	
	if 'id' not in data_json:
		data_json['id'] = id
	
	data = json.dumps(data_json)

	path = os.path.dirname(os.path.abspath(__file__))
	file_path = path + '/static/json/' + id + '.json'
	file_json = open(file_path,'w')
	file_json.write(data)
	file_json.close()

	return "ok"


@app.route("/")
def home():
	return redirect('/static/index.html', code=302)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0', port=80)
