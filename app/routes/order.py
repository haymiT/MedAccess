# app/routes/order.py
from flask import Blueprint, request, jsonify
from app.models import db, Order, Pharmacy, Supplier

order_bp = Blueprint('order_bp', __name__)

# Get all orders
@order_bp.route('/orders', methods=['GET'])
def get_orders():
    """
    Get all orders.
    
    **Endpoint:** `/orders`
    
    **Method:** `GET`
    
    **Response:**
    - `200 OK`: Returns a list of all orders.
    - `500 Internal Server Error`: If there is an error retrieving the orders.
    
    **Example Response:**
    ```json
    [
        {
            "order_id": "123",
            "pharmacy_id": "1",
            "supplier_id": "2",
            "order_date": "2023-10-01",
            "order_status": "Pending",
            "item_name": "Medication A",
            "quantity": 10
        },
        ...
    ]
    ```
    """
    orders = Order.query.all()
    all_orders = [order.to_dict() for order in orders]
    return jsonify(all_orders)

# Get a single order by order_id
@order_bp.route('/orders/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get a single order by order_id.
    
    **Endpoint:** `/orders/<order_id>`
    
    **Method:** [`GET`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A37%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forder_items.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A23%2C%22character%22%3A48%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A30%2C%22character%22%3A46%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition")
    
    **Path Parameters:**
    - [`order_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A15%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A19%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the order to retrieve.
    
    **Response:**
    - `200 OK`: Returns the order details.
    - `404 Not Found`: If the order with the specified ID does not exist.
    
    **Example Response:**
    ```json
    {
        "order_id": "123",
        "pharmacy_id": "1",
        "supplier_id": "2",
        "order_date": "2023-10-01",
        "order_status": "Pending",
        "item_name": "Medication A",
        "quantity": 10
    }
    ```
    """
    order = Order.query.filter_by(order_id=order_id).first_or_404()
    ord = order.to_dict()
    return jsonify(ord)

# Create a new order
@order_bp.route('/orders/new', methods=['POST'])
def create_order():
    """
    Create a new order.
    
    **Endpoint:** `/orders/new`
    
    **Method:** [`POST`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A41%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A103%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forder_items.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A48%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A32%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition")
    
    **Request Body:**
    - [`order_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A15%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A19%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the order.
    - [`pharmacy_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A4%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the pharmacy.
    - [`supplier_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A27%2C%22character%22%3A4%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the supplier.
    - [`order_date`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A28%2C%22character%22%3A4%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The date of the order.
    - [`order_status`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A29%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A22%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The status of the order.
    - [`item_name`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A30%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A20%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The name of the item.
    - [`quantity`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A12%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A25%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forder_items.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A14%2C%22character%22%3A30%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (integer): The quantity of the item.
    
    **Response:**
    - `201 Created`: If the order is created successfully.
    - `500 Internal Server Error`: If there is an error creating the order.
    
    **Example Response:**
    ```json
    {
        "message": "Order created successfully!"
    }
    ```
    """
    data = request.get_json() if request.is_json else request.form
    
    order_id = data.get('order_id')
    pharmacy_id = data.get('pharmacy_id')
    supplier_id = data.get('supplier_id')
    order_date = data.get('order_date')
    order_status = data.get('order_status')
    item_name = data.get('item_name')
    quantity = data.get('quantity')

    new_order = Order(
        order_id=order_id,
        pharmacy_id=pharmacy_id,
        supplier_id=supplier_id,
        order_date=order_date,
        order_status=order_status,
        item_name=item_name,
        quantity=quantity
    )

    try:
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating order: {e}'}), 500

# Update an existing order
@order_bp.route('/orders/<string:order_id>/edit', methods=['POST'])
def update_order(order_id):
    """
    Update an existing order.
    
    **Endpoint:** `/orders/<order_id>/edit`
    
    **Method:** [`POST`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A41%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A103%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forder_items.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A48%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A32%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition")
    
    **Path Parameters:**
    - [`order_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A15%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A19%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the order to update.
    
    **Request Body:**
    - [`pharmacy_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A4%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the pharmacy.
    - [`supplier_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A27%2C%22character%22%3A4%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the supplier.
    - [`order_date`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A28%2C%22character%22%3A4%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The date of the order.
    - [`order_status`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A29%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A22%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The status of the order.
    - [`item_name`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A30%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A20%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The name of the item.
    - [`quantity`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A12%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A25%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forder_items.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A14%2C%22character%22%3A30%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (integer): The quantity of the item.
    
    **Response:**
    - `200 OK`: If the order is updated successfully.
    - `404 Not Found`: If the order with the specified ID does not exist.
    - `500 Internal Server Error`: If there is an error updating the order.
    
    **Example Response:**
    ```json
    {
        "message": "Order updated successfully!"
    }
    ```
    """
    order = Order.query.filter_by(order_id=order_id).first_or_404()
    data = request.get_json() if request.is_json else request.form
    
    order.pharmacy_id = data.get('pharmacy_id')
    order.supplier_id = data.get('supplier_id')
    order.order_date = data.get('order_date')
    order.order_status = data.get('order_status')
    order.item_name = data.get('item_name')
    order.quantity = data.get('quantity')

    try:
        db.session.commit()
        return jsonify({'message': 'Order updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating order: {e}'}), 500

# Delete an order
@order_bp.route('/orders/<string:order_id>/delete', methods=['POST'])
def delete_order(order_id):
    """
    Delete an order.
    
    **Endpoint:** `/orders/<order_id>/delete`
    
    **Method:** [`POST`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A21%2C%22character%22%3A41%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A26%2C%22character%22%3A103%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forder_items.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A48%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A32%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition")
    
    **Path Parameters:**
    - [`order_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Froutes%2Forder.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A15%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess-backend%2Froutes%2Forders.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A31%2C%22character%22%3A14%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fbeki%2FMedAccess%2Fmedaccess%2Fapp%2Ftemplates%2Forder%2Findex.html%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A19%2C%22character%22%3A25%7D%7D%5D%2C%224f97ccd3-addb-46ef-92ee-75a18d919b7d%22%5D "Go to definition") (string): The ID of the order to delete.
    
    **Response:**
    - `200 OK`: If the order is deleted successfully.
    - `404 Not Found`: If the order with the specified ID does not exist.
    - `500 Internal Server Error`: If there is an error deleting the order.
    
    **Example Response:**
    ```json
    {
        "message": "Order deleted successfully!"
    }
    ```
    """
    order = Order.query.filter_by(order_id=order_id).first_or_404()

    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error deleting order: {e}'}), 500