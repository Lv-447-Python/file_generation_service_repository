import pika
import json
import rabbitmq_config

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(
    queue=rabbitmq_config.file_generation_queue_name, durable=True)

message = {'user_id': 35, 'file_id': 7, 'filter_id': 1}

channel.basic_publish(exchange='',
                      routing_key=rabbitmq_config.file_generation_queue_name,
                      body=json.dumps(message),
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                          content_type='aplication/json',
                      ))

print(" [x] Send to queue ")

connection.close()
