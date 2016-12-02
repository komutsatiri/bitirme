# -*- coding: utf-8 -*-
from flask import Flask, jsonify, Response
from flask_restful import Resource, Api
from flask.ext.cors import CORS, cross_origin
from pymongo import MongoClient


app = Flask(__name__)
CORS(app)
api = Api(app)
client = MongoClient('localhost',27017)
collection = client.conflict_db.events

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

@app.route('/dyad_name/<int:dyad_new_id>', methods=['GET'])    
@app.route('/dyad_names', defaults={'dyad_new_id': None}, methods=['GET'])
def get_dyad_name(dyad_new_id):
	if dyad_new_id is  None:
		q = collection.distinct('dyad_name')
		if q:
			print q
			output = q
		else:
			print q
			output = 'No results found'	
		return jsonify({'result' : output})	
	elif dyad_new_id is not None:
		print "debug"
		q = collection.find_one({'dyad_new_id' : dyad_new_id},{'_id':False, 'dyad_name':True})
		if q:
			output = q
		else:
			output = 'No results found'
		return jsonify({'result' : output})			



if __name__ == '__main__':
    app.run(debug=True )