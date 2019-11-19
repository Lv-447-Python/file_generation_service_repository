from flask import request, jsonify
from flask_restful import Resource
from flask_api import status
from file_generation_service.configs.flask_config import api
from file_generation_service.rabbitmq.producer import start_generating_filtered_file
import random


class FileGenerationResource(Resource):

    def get(self):

        data = {
            'user_id': request.args.get('user_id', type=int),
            'file_id': request.args.get('file_id', type=int),
            'filter_id': request.args.get('filter_id', type=int)
        }

        if None in data.values():
            return 'Bad ID', 400
        else:
            start_generating_filtered_file(data)
            return 'Your request has been submitted for processing', 200



class TestFileResource(Resource):

    def get(self):

        if request.args.get('file_id', type=int) == 1:
            result = jsonify({
                'path': '/home/orik/Documents/programming/project/file_generation_service_repository/file_generation_service/static/Test_dataset_filterMe.csv',
                'msg': 'Success',
                'status': status.HTTP_200_OK})
        elif request.args.get('file_id', type=int) == 2:
            result = jsonify({
                'path': '/home/orik/Documents/programming/project/file_generation_service_repository/file_generation_service/static/Test_dataset_filterMe.xlsx',
                'msg': 'Success',
                'status': status.HTTP_200_OK})
        else:
            result = jsonify({
                'path': '',
                'msg': 'Failed',
                'status': status.HTTP_400_BAD_REQUEST})

        return result


class TestHistoryResource(Resource):

    def get(self):

        result = jsonify(
            {
                "data": {
                    "file_id": 1,
                    "filter_date": "2019-11-18T12:31:19.742327",
                    "filter_id": 1,
                    "rows_id": list(range(1,101)),
                    "user_id": 2
                },
                "errors": "",
                "status": 200
            }
        )

        return result


api.add_resource(FileGenerationResource, '/generate')
api.add_resource(TestFileResource, '/testfile')
api.add_resource(TestHistoryResource, '/testhistory')
