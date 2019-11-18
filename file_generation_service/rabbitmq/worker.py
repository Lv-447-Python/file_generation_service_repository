import pika
import json
import rabbitmq_config
from utils.csv_generator import generate_filtered_csv_file
from utils.xlsx_generator import generate_filtered_xlsx_file


def check_ext(file_path):
    return file_path.split('.')[-1]


def request_to_file_service():
    return 'file_generation_service/static/Test_dataset_filterMe.csv'


def request_to_history_service():
    return list(range(1,101))


def callback(ch, method, properties, body):

    try:
        req = json.loads(body)
        print(req)
        
    except:
        return 'smth went wrong...'


def main():

    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(
        queue=rabbitmq_config.file_generation_queue_name, durable=True)

    channel.basic_consume(
        queue=rabbitmq_config.file_generation_queue_name, on_message_callback=callback)

    channel.basic_qos(prefetch_count=1)

    channel.start_consuming()


if __name__ == "__main__":
    main()
