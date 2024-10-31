# app/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models
# from .consumer import Consumer
from .pharmacy import Pharmacy
from .supplier import Supplier
from .inventory import Inventory
from .user import User
from .medication import Medication
from .order import Order
from .sell import Sell
from .sell_item import SellItem