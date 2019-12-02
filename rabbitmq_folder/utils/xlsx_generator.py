"""Module for generation new xls/xlsx files"""
import pandas
from utils.path_generator import new_path_generator


def generate_filtered_xlsx_file(file_path, rows_id):
    """
    The method generates a new xlsx file,
    based on the old one, and the line numbers that should be in the new one.
    Args:
        file_path:
            Path to the file.
        rows_id:
            The line numbers that should be in the new file.
    Returns:
        new_file_path:
            The path to the file that was generated.
    """

    data = pandas.read_excel(file_path)

    df = pandas.DataFrame(data)

    filtered_data = df[df['ID'].isin(rows_id)]

    new_file_path = new_path_generator(file_path)

    filtered_data.to_excel(new_file_path, index=False, header=True)

    return new_file_path
