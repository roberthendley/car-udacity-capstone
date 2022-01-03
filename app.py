from werkzeug.test import TestResponse
from api import create_app
from config import ProdConfig, DevConfig, TestConfig
import os

if os.getenv('FLASK_ENV') == 'production':
    config = ProdConfig 
elif os.getenv('FLASK_ENV') == 'testing':
    config = TestConfig
else:
    config = DevConfig

app = create_app(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)