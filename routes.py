#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Luan Rafael'

from flask import Flask
from flask import Flask, request, redirect

import json
import glob
import os

app = Flask(__name__)


@app.route("/getSiders")
def get_spiders():

	json_paths = glob.glob("static/json/*.json")

	output = []
	for json_path in json_paths:
		with open(json_path, 'r') as file:
			data = json.loads(file.read())
		output.append(data)

	return json.dumps(output)


@app.route("/api/v1/spider/<id>", methods=['POST'])
def update_spider(id):
	print('####' + id)

	data_json = request.json
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0', port=80)
