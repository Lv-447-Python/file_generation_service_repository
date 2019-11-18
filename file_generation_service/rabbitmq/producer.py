import pika
import json
from . import rabbitmq_config


def start_generating_filtered_file(message):

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

    print(" [x] Send to queue ")

    connection.close()

if __name__ == "__main__":
    start_generating_filtered_file('fdssfdsf')