from flask import Flask
import crochet

crochet.setup()

def create_app(config):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
    )

    from .views import bp
    app.register_blueprint(bp)

    return app