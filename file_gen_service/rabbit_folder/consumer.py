"""Module which pull message from rabbitmq queue"""
import pika

from file_gen_service.rabbit_folder import worker
from file_gen_service.configs import rabbitmq_config
from file_gen_service.configs.logger import logger


def main():
    """
    A function that connects to rabbitmq.
    """

    credentials = pika.PlainCredentials('admin', 'admin')

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost', 5672, '/', credentials))

    logger.info(' [x] Connection created ')
    print('[x] Connection created.')
    channel = connection.channel()

    channel.queue_declare(
        queue=rabbitmq_config.file_generation_queue_name, durable=True)

    channel.basic_consume(
        queue=rabbitmq_config.file_generation_queue_name, on_message_callback=worker.callback, auto_ack=True)

    channel.basic_qos(prefetch_count=1)

    logger.info(' [x] Start consuming ')

    channel.start_consuming()


if __name__ == "__main__":
    main()
