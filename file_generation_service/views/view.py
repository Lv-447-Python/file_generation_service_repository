from flask import request, jsonify
from flask_restful import Resource
from flask_api import status
from file_generation_service.configs.flask_config import api
from file_generation_service.rabbitmq.producer import start_generating_filtered_file


class FileGenerationResource(Resource):

    def get(self):

        data = {
            'user_id'   : request.args.get('user_id', type=int),
            'file_id'   : request.args.get('user_id', type=int),
            'filter_id' : request.args.get('filter_id', type=int)
        }
        if None in data.values():
            return status.HTTP_400_BAD_REQUEST
        else:
            start_generating_filtered_file(data)


api.add_resource(FileGenerationResource, '/generate')