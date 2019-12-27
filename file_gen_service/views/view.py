"""Module for file generation resource"""
from flask import request, jsonify
from flask_restful import Resource
from file_gen_service import API
from file_gen_service.rabbit_folder.producer import start_generating_filtered_file
from file_gen_service.configs.logger import LOGGER


class FileGenerationResource(Resource):
    """File generation resource class."""

    @staticmethod
    def existence_check(file_id, filter_id):

        result = requests.get(
            url='http://web-sharing:5000/download',
            headers={
                'filter_id': filter_id,
                'input_file_id': file_id
            }
        )
        if result.status_code == 302:
            return True
        else:
            return False

    def get(self, file_id, filter_id):
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
            "session": request.cookies['session'],
            "file_id": file_id,
            "filter_id": filter_id
        }

        if None in data.values():
            LOGGER.error('Bad ID in %s', data)
            return make_response(
                jsonify({
                    'message': 'Bad id'
                }),
                status.HTTP_400_BAD_REQUEST
            )
        else:
            exist = FileGenerationResource.existence_check(file_id, filter_id)
            if exist:
                return make_response(
                    jsonify({
                        'message': 'File already exist'
                    }),
                    status.HTTP_302_FOUND
                )
            else:
                start_generating_filtered_file(data)
                LOGGER.info('Start generating file to: %s', data)
                return make_response(
                    jsonify({
                        'message': 'Start generating file'
                    }),
                    status.HTTP_201_CREATED
                )


API.add_resource(FileGenerationResource,
                 '/file-generation/api/generate_new_file/file/<int:file_id>/filter/<int:filter_id>')
