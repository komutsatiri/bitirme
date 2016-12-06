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

@app.route('/merhaba', methods=['GET'])
def hello_world():
	output = 'Merhaba !'
	return jsonify({'result' : output})

@app.route('/markers', methods=['GET'])
def get_markers():
	output = []
	for q in collection.find({},{'_id':False}).sort([('year',1)]).limit(4000):
		output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'],
						'dyad_new_id' : q['dyad_new_id'], 'time' : q['date_start']})
	return jsonify({'result' : output})

@app.route('/details/<int:event_id>', methods=['GET'])
def get_details(event_id):
	q = collection.find_one({'id': event_id},{'_id':False})
	if q:
		output = {'source_article' : q['source_article']}
	else:
		print q
		output = 'No results found'	
	return jsonify({'result' : output})

@app.route('/dyads', methods=['GET'])
def get_dyads():
	output = {}
	ids = collection.distinct('dyad_new_id')
	names = collection.distinct('dyad_name')
	#alltaki satiri degistir try-catch ekle
	if (ids is not None) & (names is not None):
		for q,w in enumerate(ids):
			output[w] = names[q]	
	else:
		output = 'No results found'	
	return jsonify({'result' : output})	

if __name__ == '__main__':
    app.run(debug=True )