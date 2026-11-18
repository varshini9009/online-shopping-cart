# Online Shopping Cart Management System

## Project Description
The Online Shopping Cart Management System is a console-based application developed using Python and MySQL. It allows users to manage product stock, add products to a shopping cart, update or remove cart items, calculate purchase totals, apply discounts, and complete checkout while automatically updating available stock.

## Features

- **Add Products to Stock:** Add new products with quantity and price.
- **Manage Existing Stock:** Increase the quantity of existing products.
- **Add to Cart:** Add available products and their quantities to the shopping cart.
- **Delete Cart Items:** Remove products from the cart.
- **Update Cart Quantity:** Modify product quantities while checking stock availability.
- **Calculate Total:** Calculate the total purchase amount based on product prices and quantities.
- **Apply Discount:** Calculate discounts based on the purchase amount.
- **Checkout:** Validate stock availability, calculate the final amount, update stock quantities, and clear the cart.
- **Transaction Handling:** Use database transactions and rollback to prevent incomplete checkout updates.

## Technologies Used
- Python
- MySQL
- MySQL Connector/Python

## Project Structure
```text
online-shopping-cart/
│
├── main.py
├── shopping_db.sql
├── requirements.txt
|__.env.example
└── README.md
```

## Database Structure
The application uses MySQL with two main tables:

- **Stock:** Stores product names, available quantities, and prices.
- **Cart:** Stores products added to the shopping cart and their quantities.

## Discount Calculation
- Purchases above ₹1,000 receive a 20% discount during checkout.
- Purchases of ₹1,000 or below do not receive a discount.

## Installation and Setup


1. Navigate to the project folder:
   ```bash
   cd online-shopping-cart
   ```

2. Install the required package:
   ```bash
   pip install mysql-connector-python
   ```

3. Create the MySQL database and tables using the SQL setup file.

4. Update the database connection details in `create_connection()` in `main.py`.

5. Run the application:
   ```bash
   python main.py
   ```

## Learning Outcomes
- Connecting Python applications with MySQL.
- Performing CRUD operations using SQL queries.
- Working with SQL joins.
- Managing shopping cart operations.
- Implementing conditional discount calculations.
- Using database transactions, commit, and rollback.
- Maintaining stock consistency during checkout.