"""Module for file generation resource"""
from flask import request, jsonify
from flask_restful import Resource
from file_gen_service import api
from file_gen_service.rabbit_folder.producer import start_generating_filtered_file


class FileGenerationResource(Resource):
    """File generation resource class."""

    def get(self, user_id, file_id, filter_id):
        """
        Method for HTTP GET method working out. Used for start generation filtered file.
        Args:
            user_id:
                User identifier.
            file_id:
                File identifier.
            filter_id:
                Filter identifier.
        Returns:
            Message and status code.
        """

        data = {
            'user_id': user_id,
            'file_id': file_id,
            'filter_id': filter_id
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
                'path': '/file_generation_service_repo/file_generation_service/static/Test_dataset_filterMe.csv',
                'message': 'Success'})
        elif request.args.get('file_id', type=int) == 2:
            result = jsonify({
                'path': '/file_generation_service_repo/file_generation_service/static/Test_dataset_filterMe.xlsx',
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


api.add_resource(FileGenerationResource,
                 '/generate_new_file/user/<int:user_id>/file/<int:file_id>/filter/<int:filter_id>')
api.add_resource(TestFileResource, '/testfile')
api.add_resource(TestHistoryResource, '/testhistory')
