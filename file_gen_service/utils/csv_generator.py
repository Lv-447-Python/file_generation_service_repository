"""Module for generation new csv files"""
import pandas
from file_gen_service.configs.logger import LOGGER
from file_gen_service.utils.path_generator import new_path_generator


def generate_filtered_csv_file(file_path, rows_id):
    """
    The method generates a new csv file,
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

    data = pandas.read_csv(file_path)

    df = pandas.DataFrame(data)

    filtered_data = df.loc[set(rows_id)]

    new_file_path = new_path_generator(file_path)

    filtered_data.to_csv(new_file_path, index=False, header=True)

    LOGGER.info('New file path: %s', new_file_path)

    return new_file_path
