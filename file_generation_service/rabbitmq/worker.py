"""Module for generating filtered file"""
import json
import logging.config

import pika
import requests

from file_generation_service.configs import rabbitmq_config
from file_generation_service.rabbitmq.utils.csv_generator import generate_filtered_csv_file
from file_generation_service.rabbitmq.utils.xlsx_generator import generate_filtered_xlsx_file

logging.config.fileConfig('/home/orik/Documents/programming/project/file_generation_service_repository/file_generation_service/configs/logging.conf')
logger = logging.getLogger('fileGenApp')


def check_ext(file_path):
    """
    Method for checking extension of file.
    Args:
        file_path:
            The path to the file whose extension is being scanned.
    Returns:
        ext:
            File extension.
    """
    try:
        ext = file_path.split('.')[-1]
    except AttributeError:
        logger.error('Poor file name...')
        return None
    return ext


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
    # result_of_request = requests.get(f'http://localhost:5000/file?file_id={file_id}')

    if result_of_request.status_code == 200:
        data = result_of_request.json()
        logger.info('Success request to file service')
        file_path = data['path']
        return file_path
    else:
        logger.error('Error request to file service')
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
    #     f'http://localhost:5000/history?user_id={user_id}&file_id={file_id}&filter_id={filter_id}')

    if result_of_request.status_code == 200:
        data = result_of_request.json()
        logger.info('Success request to history service')
        rows_id = data['rows_id']
        return rows_id
    else:
        logger.error('Error request to history service')
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

    # logging.config.fileConfig('./logging.conf')
    # logger = logging.getLogger('FileGenApp')

    req = json.loads(body)
    user_id = req['user_id']
    file_id = req['file_id']
    filter_id = req['filter_id']

    try:
        file_path = request_to_file_service(file_id)
        rows_id = request_to_history_service(user_id, file_id, filter_id)
    except TypeError:
        logger.error('Poor response from services...')
        return None

    if check_ext(file_path) == 'csv':
        new_file_path = generate_filtered_csv_file(file_path, rows_id)
    elif check_ext(file_path) in ['xls', 'xlsx']:
        new_file_path = generate_filtered_xlsx_file(file_path, rows_id)
    else:
        logger.error('Poor file name...')
        return None

    logger.info('New file path: %s', new_file_path)
    return new_file_path


def main():
    """
    A function that connects to rabbitmq.
    """

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))

    logger.info(' [x] Connection created ')

    channel = connection.channel()

    channel.queue_declare(
        queue=rabbitmq_config.file_generation_queue_name, durable=True)

    channel.basic_consume(
        queue=rabbitmq_config.file_generation_queue_name, on_message_callback=callback, auto_ack=True)

    channel.basic_qos(prefetch_count=1)

    logger.info(' [x] Start consuming ')

    channel.start_consuming()


if __name__ == "__main__":
    main()
