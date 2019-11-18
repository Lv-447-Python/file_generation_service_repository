import pika
import json
import requests
import werkzeug.exceptions
import rabbitmq_config
from utils.csv_generator import generate_filtered_csv_file
from utils.xlsx_generator import generate_filtered_xlsx_file


def check_ext(file_path):
    return file_path.split('.')[-1]


def request_to_file_service():

    result_of_request = requests.get('http://localhost:5000/testfile')

    data = result_of_request.json()

    return data



    # return 'file_generation_service/static/Test_dataset_filterMe.csv'


def request_to_history_service():
    
    result_of_request = requests.get('http://localhost:5000/testhistory')

    data = result_of_request.json()

    return data




def callback(ch, method, properties, body):

    try:
        req = json.loads(body)
        # user_id = req['user_id']
        # file_id = req['file_id']
        # filter_id = req['filter_id']

        file_path = request_to_file_service()
        rows_id = request_to_history_service()

        print(req)
        print(file_path)
        print(rows_id)

    except:
        print('smth went wrong...')


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
