import logging
import os
import os.path
from datetime import datetime
# from app.logger import Logger,


from app import init_app

app = init_app()


def config_logger():
    logs_directory = os.path.dirname(os.path.join(os.getcwd(), 'logs/'))

    if not os.path.exists(logs_directory):
        os.mkdir(path=logs_directory)

    log_file_name = f"{datetime.today().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(logs_directory, log_file_name)

    formatter = logging.Formatter('%(asctime)s %(levelname)s:  %(message)s', '%H:%M:%S')

    werkzeug = logging.getLogger('werkzeug')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    werkzeug.addHandler(console_handler)
    werkzeug.addHandler(file_handler)
    werkzeug.removeHandler('wsgi')

    return werkzeug


logger = config_logger()

if __name__ == '__main__':
    app.run(debug=False)
