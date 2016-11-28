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
	for q in collection.find({},{'_id':False}).limit(4000):
		output.append({'id' : q['id'], 'lat' : q['latitude'], 'lon' : q['longitude'], 'dyad_new_id' : q['dyad_new_id']})
	return jsonify({'results' : output})

@app.route('/details/<int:event_id>', methods=['GET'])
def get_details(event_id):
	q = collection.find_one({'id': event_id},{'_id':False})
	if q:
		output = {'source_article' : q['source_article']}
	else:
		print q
		output = 'No results found'	
	return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True )