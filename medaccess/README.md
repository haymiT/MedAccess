# MedAccess Project
### Overview
MedAccess is a pharmacy management system that allows users to manage inventory, orders, medications, suppliers, consumers, and pharmacies efficiently.

### Project Structure

medaccess/
├── app
│   ├── config.py
│   ├── database.py
│   ├── __init__.py
│   ├── models
│   │   ├── consumer.py
│   │   ├── __init__.py
│   │   ├── inventory.py
│   │   ├── medication.py
│   │   ├── order.py
│   │   ├── pharmacy.py
│   │   ├── supplier.py
│   │   └── user.py
│   ├── routes
│   │   ├── consumer.py
│   │   ├── __init__.py
│   │   ├── inventory.py
│   │   ├── medication.py
│   │   ├── order.py
│   │   ├── pharmacy.py
│   │   ├── supplier.py
│   │   └── user.py
│   └── templates
│       ├── consumer
│       │   ├── create.html
│       │   ├── index.html
│       │   ├── update.html
│       │   └── view.html
│       ├── home.html
│       ├── inventory
│       │   ├── create.html
│       │   ├── index.html
│       │   ├── pharmacy_details.html
│       │   ├── search.html
│       │   ├── search_results.html
│       │   ├── search_results_partial.html
│       │   ├── update.html
│       │   └── view.html
│       ├── layout.html
│       ├── medication
│       │   ├── create.html
│       │   ├── index.html
│       │   ├── kk.html
│       │   ├── search.html
│       │   ├── search_results.html
│       │   ├── update.html
│       │   └── view.html
│       ├── order
│       │   ├── create.html
│       │   ├── index.html
│       │   ├── update.html
│       │   └── view.html
│       ├── pharmacy
│       │   ├── create.html
│       │   ├── index.html
│       │   ├── update.html
│       │   └── view.html
│       ├── supplier
│       │   ├── create.html
│       │   ├── index.html
│       │   ├── update.html
│       │   └── view.html
│       └── user
│           ├── create.html
│           ├── index.html
│           ├── update.html
│           └── view.html
├── initialize_db.py
├── README.md
├── requirements.txt
├── run.py
├── static
│   ├── css
│   │   └── style.css
│   ├── images
│   └── js
├── to_create_table
└── to_migrate_database

## How to Run This Application
### Step 1: Clone the Repository

    git clone https://github.com/haymiT/MedAccess.git

#### Navigate to the medaccess directory

    cd medaccess
### Step 2: Install Requirements
Install the necessary dependencies:

    pip install -r requirements.txt

### Step 3: Setup the Database
Create a database (replace 'your_database_name' with your desired database name):

    CREATE DATABASE your_database_name;

Create a database user with a password and grant all privileges:

    CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
    GRANT ALL PRIVILEGES ON your_database_name.* TO 'your_username'@'localhost';
    FLUSH PRIVILEGES;

### Step 4: Create a .env File
Create a .env file in the project root directory and add your database connection string and secret key:

    SECRET_KEY=xyxyxyyyxy
    DATABASE_URL=mysql+pymysql://   your_username:your_password@localhost/your_database_name

### Step 5: Create Database Tables
To create all of your tables inside the database, run:

    python3 initialize_db.py

### Step 6: Handle Migrations
Once your tables are created, if you make any changes to your models, use the following commands to migrate:

    flask db migrate -m "database migration"
    flask db upgrade

### Step 7: Run the Application
To start the application, run the following command in the project's home directory:

    python3 run.py

You will see the following output:

    * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 718-483-512

### Step 8: Open in Browser
Open your browser and navigate to:

    http://127.0.0.1:5000

Since there is no API route for the home page, you will see:

    Not Found
    The requested URL was not found on the server. If you entered the URL manually, please check your spelling and try again.

To access the app, append an API route to the URL, for example:

    http://127.0.0.1:5000/inventory

Now you should see the navigation menu and be able to use the application. Enjoy!