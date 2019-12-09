"""Module for file generation resource"""
from flask import request, jsonify
from flask_restful import Resource
from file_generation_service import api
from rabbitmq_folder.producer import start_generating_filtered_file


class FileGenerationResource(Resource):
    """File generation resource class."""

    def get(self):
        """
        Method for HTTP GET method working out. Used for start generation filtered file.
        Returns:
            Message and status code.
        """

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
    """Test file resource"""
    def get(self):
        """
        Method for HTTP GET method working out. Used for start generation filtered file.
        Returns:
            Json file with path to file, message and status code.
        """

        if request.args.get('file_id', type=int) == 1:
            result = jsonify({
                'path': './static/Test_dataset_filterMe.csv',
                'message': 'Success'})
        elif request.args.get('file_id', type=int) == 2:
            result = jsonify({
                'path': './static/Test_dataset_filterMe.xlsx',
                'message': 'Success'})
        else:
            result = jsonify({
                'error': 'File with such id not found'
            })

        return result


class TestHistoryResource(Resource):
    """Test history resource"""

    def get(self):
        """
        Method for HTTP GET method working out. Used for start generation filtered file.
        Returns:
            Json file rows_id message and status code.
        """

        result = jsonify(
            {
                'user_id': 1,
                'file_id': 2,
                'filter_id': 3,
                'rows_id': list(range(1, 500, 3)),
                'date': 12345
            }
        )

        return result


api.add_resource(FileGenerationResource, '/generate')
api.add_resource(TestFileResource, '/testfile')
api.add_resource(TestHistoryResource, '/testhistory')
