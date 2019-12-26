#!usr/bin/env python
"""Module for generating filtered file"""
import json
from flask import send_file, send_from_directory, safe_join, abort
import requests
from file_gen_service.utils.csv_generator import generate_filtered_csv_file
from file_gen_service.utils.xlsx_generator import generate_filtered_xlsx_file
from file_gen_service.configs.logger import LOGGER


def post_request_to_sharing_service(file_path):
    sharing_url = "http://web-sharing:5000/file-sharing/api/download"
    try:
        file = open(file_path, 'rb')
        file_to_load = {'generated_file': file}
    except FileNotFoundError as err:
        LOGGER.error(err)
        LOGGER.error("----------------CANT'T OPEN FILE")

    result = requests.post(
        url=sharing_url,
        files=file_to_load
    )

def request_to_file_service(file_id):
    """
    The method for request to file service, to get the path to the file.
    Args:
        file_id:
            The ID of the file you want to get.
    Returns:
        file_path:
            The path to the file.
    """

    result_of_request = requests.get(
        url=f'http://web-file:5000/file-service/api/file/{file_id}'
    )

    if result_of_request.status_code == 200:
        data = result_of_request.json()
        LOGGER.info('Success request to file service')
        file_path = data['path']
        return file_path
    else:
        LOGGER.error('Error request to file service')
        return None


def request_to_history_service(session, file_id, filter_id):
    """
    The method for request to history service, to get the rows id of the filtered file.
    Args:
        session:
            The user session for which you want to get filtered rows.
        file_id:
            The ID of the file you want to get.
        filter_id:
            The filter ID for which you want to get the filtered rows.
    Returns:
        rows_id:
            The line numbers that were obtained after filtering the file by the user.
    """

    result_of_request = requests.get(
        url=f'http://web-history:5000/history-service/api/history/file/{file_id}/filter/{filter_id}',
        cookies={'session': session}
    )
    if result_of_request.status_code == 200:
        data = result_of_request.json()
        LOGGER.info('Success request to history service')
        rows_id = data['rows_id']
        return rows_id
    else:
        LOGGER.error('Error request to history service')
        return None

def callback(ch, method, properties, body):
    """
    A function that is called when a message is received from a queue
    and performs basic manipulations, ie requests to other services
    and a call to functions that will generate a new file.
    Args:
        ch:
            Virtual connection, inside another connection between producer and consumer.
        method:
            Method of data transmission between producer and consumer.
        properties:
            pika.spec.BasicProperties
        body:
            The message, in bytes, that is transmitted between the producer and the consumer.
    Returns:
        new_file_path:
            The path to the generated file.
    """

    req = json.loads(body)
    session = req['session']
    file_id = req['file_id']
    filter_id = req['filter_id']

    try:
        file_path = request_to_file_service(file_id)
        rows_id = request_to_history_service(session, file_id, filter_id)
    except TypeError:
        LOGGER.error('Poor response from services...')
        return None

    if file_path.endswith('csv'):
        new_file_path = generate_filtered_csv_file(file_path, rows_id)
    elif file_path.endswith(('xls', 'xlsx')):
        new_file_path = generate_filtered_xlsx_file(file_path, rows_id)
    else:
        LOGGER.error('Poor file name...')
        return None

    sharing_response = post_request_to_sharing_service(new_file_path)
    # file_response = post_request_to_file_service(new_file_path)

    # LOGGER.info(f'-------------------- File response in FILEGENAPP {file_response.status_code}')
    # TODO: push to notification and sharing
    return new_file_path
