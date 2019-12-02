"""Module for running Flask app"""
from file_generation_service import app
from file_generation_service.views import view

if __name__ == "__main__":
    app.run(debug=True)
