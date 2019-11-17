import pika
import json
import rabbitmq_config

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(
    queue=rabbitmq_config.file_generation_queue_name, durable=True)


def callback(ch, method, properties, body):

    req = json.loads(body)
    print(" [x] Recived ", req['user_id'])




channel.basic_consume(
    queue=rabbitmq_config.file_generation_queue_name, on_message_callback=callback)
channel.basic_qos(prefetch_count=1)

channel.start_consuming()
