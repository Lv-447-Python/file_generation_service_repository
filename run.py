"""Module for running Flask app"""
from file_gen_service import APP
from file_gen_service.views import view


@APP.route('/')
def test_hello():
    return 'Hello World!'


if __name__ == "__main__":
    APP.run(debug=True, host='0.0.0.0')
