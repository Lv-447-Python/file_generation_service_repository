"""Module which push message into rabbitmq queue"""
import json
import pika
from rabbitmq_folder.configs import rabbitmq_config
from logger.logger import logger


def start_generating_filtered_file(message):
    """
    A function that connects to rabbitmq and push message to the queue.
    Args:
        message:
            A message from view (json)
    """

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(
        queue=rabbitmq_config.file_generation_queue_name, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=rabbitmq_config.file_generation_routing_key,
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                              content_type='aplication/json',
                          ))

    logger.info(" [x] Send to queue ")

    connection.close()
