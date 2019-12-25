"""Module which push message into rabbitmq queue"""
import json

import pika

from file_gen_service.configs import rabbitmq_config
from file_gen_service.configs.logger import LOGGER


def start_generating_filtered_file(message):
    """
    A function that connects to rabbitmq and push message to the queue.
    Args:
        message:
            A message from view (json)
    """

    credentials = pika.PlainCredentials('admin', 'admin')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
    channel = connection.channel()
    channel.queue_declare(
        queue=rabbitmq_config.file_generation_queue_name)

    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_config.file_generation_routing_key,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                              content_type='aplication/json',
                          ))

    LOGGER.info("Send message:%s to queue:%s", message, rabbitmq_config.file_generation_queue_name)

    connection.close()
