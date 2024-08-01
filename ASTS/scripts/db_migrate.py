# Your database migration script here

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import logging

logger = logging.getLogger(__name__)

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)
    return app

def migrate_database():
    app = create_app('server-config.py')
    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()
        logger.info("Database migration completed.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    migrate_database()
