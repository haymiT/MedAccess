from flask import Flask
from app.models import db
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # CORS Configuration with credentials and explicit methods allowed
    cors = CORS(app, resources={r"/*": {"origins": "http://localhost:6445"}}, supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Set static folder
    app.static_folder = 'static'

    # Register blueprints for each route
    from app.routes.pharmacy import pharmacy_bp
    from app.routes.supplier import supplier_bp
    from app.routes.inventory import inventory_bp
    from app.routes.user import user_bp
    from app.routes.medication import medication_bp
    from app.routes.order import order_bp
    from app.routes.sell import sell_bp

    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(medication_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(sell_bp)

    # Allow credentials in responses
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:6445')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

    return app
