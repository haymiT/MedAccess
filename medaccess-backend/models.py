from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geography
from geoalchemy2 import Geometry

db = SQLAlchemy()

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    userEmail = db.Column(db.String(255), unique=True, nullable=False)
    userPassword = db.Column(db.String(255), nullable=False)
    userType = db.Column(db.Enum('customer', 'pharmacy', 'supplier'), nullable=False)
    userPhoneNumber = db.Column(db.String(15))
    userPhoneVerified = db.Column(db.Boolean, default=False)
    userEmailVerified = db.Column(db.Boolean, default=False)
    userCreatedAt = db.Column(db.DateTime, default=db.func.now())
    userUpdatedAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Customer(db.Model):
    customerID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

# class Pharmacy(db.Model):
#     __tablename__ = 'pharmacies'
#     pharmacyID = db.Column(db.Integer, primary_key=True)
#     userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
#     pharmacyName = db.Column(db.String(255), nullable=False)
#     licenseNumber = db.Column(db.String(255), nullable=False)
#     openingHours = db.Column(db.String(50))
#     location = db.Column(db.Point, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Pharmacy(db.Model):
    __tablename__ = 'pharmacies'
    
    pharmacyID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'), nullable=False)
    pharmacyName = db.Column(db.String(255), nullable=False)
    licenseNumber = db.Column(db.String(255), nullable=False)
    openingHours = db.Column(db.String(50))
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, userID, pharmacyName, licenseNumber, openingHours, location):
        self.userID = userID
        self.pharmacyName = pharmacyName
        self.licenseNumber = licenseNumber
        self.openingHours = openingHours
        self.location = location

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplierID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    supplierName = db.Column(db.String(255), nullable=False)
    licenseNumber = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255))
    location = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=False) 
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Medication(db.Model):
    medicationID = db.Column(db.Integer, primary_key=True)
    medicationAddedBy = db.Column(db.Integer, db.ForeignKey('user.userID'))
    medicationName = db.Column(db.String(255), nullable=False)
    medicationDescription = db.Column(db.Text)
    medicationDosage = db.Column(db.String(50))
    medicationPrice = db.Column(db.Numeric(10, 2))
    medicationManufactureDate = db.Column(db.Date)
    medicationExpireDate = db.Column(db.Date)
    medicationMadeIn = db.Column(db.String(255))
    medicationCreatedAt = db.Column(db.DateTime, default=db.func.now())
    medicationUpdatedAt = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Inventory(db.Model):
    inventoryID = db.Column(db.Integer, primary_key=True)
    pharmacyID = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyID'))
    medicationID = db.Column(db.Integer, db.ForeignKey('medication.medicationID'))
    quantity = db.Column(db.Integer, nullable=False)
    reorderLevel = db.Column(db.Integer, nullable=False)
    pricePerUnit = db.Column(db.Numeric(10, 2))
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

class Order(db.Model):
    orderID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    recipientID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    orderType = db.Column(db.Enum('customer_order', 'pharmacy_order'))
    orderStatus = db.Column(db.Enum('pending', 'shipped', 'completed', 'canceled'))
    totalAmount = db.Column(db.Numeric(10, 2))
    orderDate = db.Column(db.DateTime, default=db.func.now())
    deliveryDate = db.Column(db.DateTime)

class OrderItem(db.Model):
    orderItemID = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('order.orderID'))
    medicationID = db.Column(db.Integer, db.ForeignKey('medication.medicationID'))
    quantity = db.Column(db.Integer, nullable=False)
    pricePerUnit = db.Column(db.Numeric(10, 2))
    totalPrice = db.Column(db.Numeric(10, 2))

class SearchHistory(db.Model):
    searchID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    medicationID = db.Column(db.Integer, db.ForeignKey('medication.medicationID'))
    searchTimestamp = db.Column(db.DateTime, default=db.func.now())
    resultCount = db.Column(db.Integer)

class Alert(db.Model):
    alertID = db.Column(db.Integer, primary_key=True)
    pharmacyID = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyID'))
    alertType = db.Column(db.Enum('low_stock', 'expiration', 'new_order'))
    alertMessage = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=db.func.now())

class Delivery(db.Model):
    deliveryID = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('order.orderID'))
    deliveryStatus = db.Column(db.Enum('pending', 'in_transit', 'delivered'))
    deliveryDate = db.Column(db.DateTime)
    deliveryAddress = db.Column(db.Text)
    trackingNumber = db.Column(db.String(255))

class Transaction(db.Model):
    transactionID = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('order.orderID'))
    transactionDate = db.Column(db.DateTime, default=db.func.now())
    amount = db.Column(db.Numeric(10, 2))
    paymentMethod = db.Column(db.Enum('bank_transfer', 'telebirr', 'mpesa', 'others'))
    transactionStatus = db.Column(db.Enum('completed', 'failed', 'pending'))

class Review(db.Model):
    reviewID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    pharmacyID = db.Column(db.Integer, db.ForeignKey('pharmacy.pharmacyID'))
    medicationID = db.Column(db.Integer, db.ForeignKey('medication.medicationID'))
    rating = db.Column(db.Integer)
    reviewText = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, default=db.func.now())
