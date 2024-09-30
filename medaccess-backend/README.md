# MedAccess Backend

## Project Description

MedAccess is a web-based platform designed to streamline the process of locating and managing medications in pharmacies. This backend application is built using Flask, a lightweight web framework for Python. It serves as the API for the MedAccess frontend and manages user authentication, medication inventory, orders, and other essential features.

## Features

- User registration and authentication
- Management of medications, pharmacies, suppliers, and orders
- Search history tracking
- Alerts for medication availability and orders
- Delivery tracking and transactions
- Review system for users and medications
- Admin management and inventory control

## Installation

To set up the backend for MedAccess, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Esubalew197/medaccess-backend.git
   cd medaccess-backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up the database (modify `config.py` if necessary).

6. Run the application:
   ```bash
   flask run
   ```

   The backend server will start running at `http://127.0.0.1:5000`.

## Usage

- The backend provides a RESTful API for the frontend to interact with.
- API endpoints are structured under the `/api` prefix (for example, `/api/users`, `/api/orders`, etc.).
- Refer to the individual route files in the `routes/` directory for available endpoints and their functionalities.

## File Structure

```
medaccess-backend/
│
├── app.py                  # Main application file
├── config.py               # Configuration settings
├── models.py               # Database models
├── __init__.py             # Package initialization
├── requirements.txt        # Required packages
├── routes/                 # API route definitions
│   ├── __init__.py
│   ├── admin.py            # Admin-related routes
│   ├── customers.py        # Customer-related routes
│   ├── inventory.py        # Inventory management routes
│   ├── users.py            # User-related routes
│   ├── orders.py           # Order-related routes
│   ├── order_items.py      # Order items-related routes
│   ├── medications.py      # Medication-related routes
│   ├── suppliers.py        # Supplier-related routes
│   ├── pharmacies.py       # Pharmacy-related routes
│   ├── search_history.py   # Search history routes
│   ├── alerts.py           # Alerts management
│   ├── delivery.py         # Delivery tracking
│   ├── transactions.py     # Transaction handling
│   └── reviews.py          # Review management
└── tests/                  # Unit tests
    ├── __init__.py
    ├── test_admin.py       # Tests for admin routes
    ├── test_customers.py   # Tests for customer routes
    ├── test_inventory.py   # Tests for inventory routes
    ├── test_users.py       # Tests for user routes
    ├── test_orders.py      # Tests for order routes
    ├── test_order_items.py # Tests for order items routes
    ├── test_medications.py # Tests for medication routes
    ├── test_reviews.py     # Tests for review routes
    ├── test_suppliers.py   # Tests for supplier routes
    ├── test_pharmacies.py  # Tests for pharmacy routes
    ├── test_search_history.py # Tests for search history routes
    ├── test_alerts.py      # Tests for alerts
    ├── test_delivery.py    # Tests for delivery
    └── test_transactions.py# Tests for transactions
```

## Testing

To run the tests, ensure you are in the virtual environment and use the following command:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

