# -*- coding: utf-8 -*-
from flask import Flask, jsonify
#from flask_restful import Resource, Api
from flask.ext.cors import CORS, cross_origin
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)
#api = Api(app)
client = MongoClient('localhost',27017)
collection = client.conflict_db.events

@app.route('/', methods=['GET'])
def hello_world():
	output = 'Hi!, give me some parameters, would you?'
	return jsonify({'result' : output})


@app.route('/markers/<int:dyad_new_id>', methods=['GET'])
@app.route('/markers', defaults={'dyad_new_id': None}, methods=['GET'])
def get_markers(dyad_new_id):
	output = []
	counter = 0
	if dyad_new_id is None:
		for q in collection.find({},{'_id':False}).sort([('year',1)]):
			output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'],
							'time' : q['date_start']})
			counter = counter + 1
		return jsonify({'result' : output, 'number of records': counter})
	elif dyad_new_id is not None:
		for q in collection.find({'dyad_new_id': dyad_new_id},{'_id':False}).sort([('year',1)]):
			output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'],
							'time' : q['date_start']})
			counter = counter + 1
		return jsonify({'result' : output, 'number of records': counter})
			
@app.route('/details/<int:event_id>', methods=['GET'])
def get_details(event_id):
	q = collection.find_one({'id': event_id,},{'_id':False})
	if q:
		output = {'source_article': q['source_article'], 'dyad_name': q['dyad_name']}
	else:
		print q
		output = 'No results found'	
	return jsonify({'result' : output})

@app.route('/dyads', methods=['GET'])
def get_dyads():
	output = {}
	counter = 0
	ids = collection.distinct('dyad_new_id')
	names = collection.distinct('dyad_name')
	#alltaki satiri degistir try-catch ekle
	if (ids is not None) & (names is not None):
		for q,w in enumerate(ids):
			output[w] = names[q]
			counter = counter + 1	
	else:
		output = 'No results found'	
	return jsonify({'result' : output, 'number of records': counter})	

if __name__ == '__main__':
    app.run(debug=True )