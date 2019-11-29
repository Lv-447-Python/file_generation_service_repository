"""Module for generation new file path"""
from datetime import datetime


def new_path_generator(file_path):
    """
    The method generates a new filename using timestamp.
    Args:
        file_path:
            Path to the file.
    Returns:
        new_file_path
            A new file path.
    """

    file_extention = file_path.split('.')[-1]
    path = file_path.split('.')[:-1]

    new_file_path = path[0] + \
        str(datetime.utcnow().strftime("_%Y%m%d_%H%M%S")) + '.' + file_extention

    return new_file_path
