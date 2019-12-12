"""Module for running Flask app"""
from file_gen_service import app


# from file_generation_service.views import view


@app.route('/')
def test_hello():
    return 'Hello World!'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
