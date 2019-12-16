#!usr/bin/env python
"""Module for generating filtered file"""
import json

import requests
from file_gen_service.utils.csv_generator import generate_filtered_csv_file
from file_gen_service.utils.xlsx_generator import generate_filtered_xlsx_file
from file_gen_service.configs.logger import LOGGER


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
        f'http://localhost:5000/testfile?file_id={file_id}')
    # result_of_request = requests.get(f'http://localhost:5000/file/{file_id}')

# TODO: check request to service

    if result_of_request.status_code == 200:
        data = result_of_request.json()
        LOGGER.info('Success request to file service')
        file_path = data['path']
        return file_path
    else:
        LOGGER.error('Error request to file service')
        return None


def request_to_history_service(user_id, file_id, filter_id):
    """
    The method for request to history service, to get the rows id of the filtered file.
    Args:
        user_id:
            The user ID for which you want to get filtered rows.
        file_id:
            The ID of the file you want to get.
        filter_id:
            The filter ID for which you want to get the filtered rows.
    Returns:
        rows_id:
            The line numbers that were obtained after filtering the file by the user.
    """

    result_of_request = requests.get('http://localhost:5000/testhistory')
    # result_of_request = requests.get(
    #     f'http://localhost:5000/history/user/{user_id}/file/{file_id}/filter/{filter_id}')
# TODO: check request to service
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
    user_id = req['user_id']
    file_id = req['file_id']
    filter_id = req['filter_id']

    try:
        file_path = request_to_file_service(file_id)
        rows_id = request_to_history_service(user_id, file_id, filter_id)
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

    LOGGER.info('New file path: %s', new_file_path)
# TODO: push to notification and sharing
    return new_file_path
