"""Module for file generation resource"""
from flask import request, jsonify
from flask_restful import Resource
from file_gen_service import API
from file_gen_service.rabbit_folder.producer import start_generating_filtered_file
from file_gen_service.configs.logger import LOGGER


class FileGenerationResource(Resource):
    """File generation resource class."""

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
            return 'Bad ID', 400
        else:
            start_generating_filtered_file(data)
            LOGGER.info('Start generating file to: %s', data)
            return 'Your request has been submitted for processing', 200


API.add_resource(FileGenerationResource,
                 '/generate_new_file/file/<int:file_id>/filter/<int:filter_id>')
