from datetime import datetime

def new_path_generator(file_path):

    file_extention = file_path.split('.')[-1]
    path = file_path.split('.')[:-1]

    new_file_path = path[0] + str(datetime.now().strftime("_%Y%m%d_%H%M%S")) + '.' + file_extention

    return new_file_path
