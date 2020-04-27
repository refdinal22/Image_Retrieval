import os
import sys
import skimage.io

import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, send_from_directory
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
from database.database import DAO

sys.path.insert(0, "../retrieval/")
from detector import Detector
import extractor

api = Api(app)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_id(query_feature):
	path = "../featureCNN_map.h5"
	h5f = h5py.File(path,'r')
	feats = h5f['feats'][:]
	id = h5f['id'][:]
	h5f.close()	
	
	# # feats.T = transformasi
	# similarity
	scores = np.dot(query_feature, feats.T)
	# sort
	rank_ID = np.argsort(scores)[::-1]

	rank_score = scores[rank_ID]
	id_rank = id[rank_ID]
	# score > 0.8
	rank = np.r_[(rank_score>0.8).nonzero()]

	id_rank = id_rank[rank]

	return id_rank


class Retrieval(Resource):	
	def post(self):
		if 'file' not in request.files:
			resp = jsonify({'message' : 'No file part in the request'})
			resp.status_code = 400
			return resp
		file = request.files['file']		

		# Save Image To Server
		filename = secure_filename(file.filename)		
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		image_path = 'image/uploads/'+filename
		# Add Detector
		image_detector = Detector("../weight/mask_rcnn_fashion.h5")
		# Add Extractor
		image_extractor = extractor.Extractor()
		# Add Database
		database = DAO()

		# Object Detection
		image = skimage.io.imread(image_path)
		detection_results = image_detector.detection(image)
		# Dominan Object
		big_object, big_ix = image_detector.get_biggest_box(detection_results['rois'])
		cropped_object = image_detector.crop_object(image, big_object)

		# Extract
		query_image_feature = image_extractor.extract_feat(cropped_object)

		# similarity
		id = get_id(query_image_feature)

		result = database.getProduct(id)
		for res in result:
			data.append(res.to_dict())
						
		resp = jsonify({'data': data})
		resp.status_code = 200
		return resp

	def get(self):
		database = DAO()
		result = database.getAll()
		data = []
		for res in result:
			data.append(res.to_dict())
			
			
		resp = jsonify({'data': data})
		resp.status_code = 200
		return resp


class ImageServer(Resource):
	def get(self, filename):
		return send_from_directory(app.static_folder, filename)

api.add_resource(Retrieval, '/retrieval/image', endpoint='image')
api.add_resource(ImageServer, '/image/<string:filename>', endpoint='get')

if __name__ == "__main__":
    app.run(debug=True)	