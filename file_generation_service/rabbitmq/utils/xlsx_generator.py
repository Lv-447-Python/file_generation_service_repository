import pandas
from .path_generator import new_path_generator


def generate_filtered_xlsx_file(file_path, rows_id):

    data = pandas.read_excel(file_path)

    df = pandas.DataFrame(data)

    filtered_data = df[df['ID'].isin(rows_id)]

    new_file_path = new_path_generator(file_path)

    filtered_data.to_excel(new_file_path, index=False, header=True)

    return new_file_path
