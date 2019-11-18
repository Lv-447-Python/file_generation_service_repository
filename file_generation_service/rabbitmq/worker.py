import pika
import json
import requests
import rabbitmq_config
from utils.csv_generator import generate_filtered_csv_file
from utils.xlsx_generator import generate_filtered_xlsx_file


def check_ext(file_path):
    return file_path.split('.')[-1]


def request_to_file_service(file_id):

    result_of_request = requests.get('http://localhost:5000/testfile')
    # result_of_request = requests.get(f'http://localhost:5000/file?file_id={file_id}')

    data = result_of_request.json()

    if data['status'] == 200:
        print(data['msg'])
        file_path = data['path']

        return file_path
    else:
        print('smth went wrong...')
        return


def request_to_history_service(user_id, file_id, filter_id):

    result_of_request = requests.get('http://localhost:5000/testhistory')
    # result_of_request = requests.get(
    #     f'http://localhost:5000/history?user_id={user_id}&file_id={file_id}&filter_id={filter_id}')

    data = result_of_request.json()

    if data['status'] == 200:
        print('Success')
        rows_id = data['data']['rows_id']

        return rows_id
    else:
        print('smth went wrong...')
        return


def callback(ch, method, properties, body):

    # try:

    req = json.loads(body)
    user_id = req['user_id']
    file_id = req['file_id']
    filter_id = req['filter_id']

    file_path = request_to_file_service(file_id)
    rows_id = request_to_history_service(user_id, file_id, filter_id)

    if check_ext(file_path) == 'csv':
        new_file_path = generate_filtered_csv_file(file_path, rows_id)
    else:
        new_file_path = generate_filtered_xlsx_file(file_path, rows_id)
    print(new_file_path)

    # except:
    #     print('smth went wrong...')


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
