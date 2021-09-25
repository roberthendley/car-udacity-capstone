from .api import create_app
from .config import ProdConfig, DevConfig
import os

config = ProdConfig if os.getenv('FLASK_ENV') == 'production' else DevConfig
app = create_app(ProdConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)