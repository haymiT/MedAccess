# app/__init__.py
from flask import Flask
from app.models import db
from flask_migrate import Migrate

from dotenv import load_dotenv
import os


load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)
    if config_name:
        app.config.from_object(config_name)
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

      # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Set static folder
    app.static_folder = 'static'

    # Register blueprints for each route (consumer, pharmacy, supplier, inventory)
    # from app.routes.consumer import consumer_bp
    from app.routes.pharmacy import pharmacy_bp
    from app.routes.supplier import supplier_bp
    from app.routes.inventory import inventory_bp
    from app.routes.user import user_bp
    from app.routes.medication import medication_bp
    from app.routes.order import order_bp
    from app.routes.sell import sell_bp
    

    # app.register_blueprint(consumer_bp)
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(medication_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(sell_bp)


    return app
