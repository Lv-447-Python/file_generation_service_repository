import pika
from configs import rabbitmq_config
import worker
# from logger.logger import logger


def main():
    """
    A function that connects to rabbitmq.
    """

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq'))

    # logger.info(' [x] Connection created ')

    channel = connection.channel()

    channel.queue_declare(
        queue=rabbitmq_config.file_generation_queue_name, durable=True)

    channel.basic_consume(
        queue=rabbitmq_config.file_generation_queue_name, on_message_callback=worker.callback, auto_ack=True)

    channel.basic_qos(prefetch_count=1)

    # logger.info(' [x] Start consuming ')

    channel.start_consuming()


if __name__ == "__main__":
    main()
