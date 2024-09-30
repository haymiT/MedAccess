from flask import Flask
from config import Config
from models import db
from routes.users import users_bp
from routes.orders import orders_bp
from routes.medications import medications_bp
from routes.suppliers import suppliers_bp
from routes.pharmacies import pharmacies_bp
from routes.search_history import search_history_bp
from routes.alerts import alerts_bp
from routes.delivery import delivery_bp
from routes.transactions import transactions_bp
from routes.reviews import reviews_bp
from routes.admin import admin_bp
from flask_cors import CORS
from flask_migrate import Migrate

# Create the app factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load the configuration
    db.init_app(app)  # Initialize the database
    CORS(app)  # Enable CORS

    migrate = Migrate(app, db)  # Initialize migration

    # Register blueprints
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(medications_bp, url_prefix='/api/medications')
    app.register_blueprint(suppliers_bp, url_prefix='/api/suppliers')
    app.register_blueprint(pharmacies_bp, url_prefix='/api/pharmacies')
    app.register_blueprint(search_history_bp, url_prefix='/api/search')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    app.register_blueprint(delivery_bp, url_prefix='/api/delivery')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(reviews_bp, url_prefix='/api/reviews')

    # @app.before_first_request
    _got_first_request = False
    def create_tables():
        db.create_all()  # Create tables before the first request

    return app

# Ensure the correct app instance is used
if __name__ == '__main__':
    app = create_app()  # Create the app instance
    app.run(debug=True)  # Run the app
