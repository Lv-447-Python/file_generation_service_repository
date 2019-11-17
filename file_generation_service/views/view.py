from flask import request
from flask_restful import Resource
from flask_api import status
from file_generation_service.configs.flask_config import api


class FileGenerationResource(Resource):

    def get(self):

        return request.args


api.add_resource(FileGenerationResource, '/generate')