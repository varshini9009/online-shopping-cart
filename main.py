import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

#function to create connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection

    except mysql.connector.Error as error:
        print("database connection error:", error)
        return None

#function to add product to cart
def add_stock():
    connection=create_connection()
    cursor=connection.cursor()
    product_name=input("enter name of the product:")
    product_quantity=int(input("enter the quantity:"))
    price=float(input("enter the price:"))
    cursor.execute("select*from stock where product_name=%s",(product_name,))
    stock=cursor.fetchone()
    if stock:
        print("product already existed.")
        print("1.add quantity")
        print("2.exit") 
        choice=input("choose your choice:")
        if choice=="1":
           product_quantity=int(input("enter the quantity:"))
           cursor.execute("update stock set product_quantity=product_quantity+%s where product_name=%s",(product_quantity,product_name)) 
           print("quantity added successfully.")
           connection.commit()
        elif choice=="2":
            print("exist.")
        else:
            print("invalid choice.")
    else:
        query="""insert into stock(product_name,product_quantity,price)values(%s,%s,%s)"""
        cursor.execute(query,(product_name,product_quantity,price))
        connection.commit()
        print("product added successfully to the store.") 
    cursor.close()
    connection.close()




           
# function to add product to cart
def add_to_cart():
    connection=create_connection()
    cursor=connection.cursor()
    product_name=input("enter the product name:")
    cursor.execute("select*from stock where product_name=%s",(product_name,))
    stock=cursor.fetchone()
    if not stock:
        print("product not existed in stock.")
    else:
        product_quantity=int(input("enter the product quantity:"))
        if product_quantity>stock[2]:
            print("no enough quantity existed.")
        else:
            cursor.execute("""insert into cart(product_name,product_quantity)values(%s,%s)""",(product_name,product_quantity))
            connection.commit()
            print("product added to cart.")
    cursor.close()
    connection.close()


#function to delete product from cart
def delete_product():
    connection=create_connection()
    cursor=connection.cursor()
    product_name=input("enter the product name:")
    cursor.execute("select*from cart where product_name=%s",(product_name,)) 
    product=cursor.fetchone()               
    if product:
        cursor.execute("delete from cart where product_name=%s",(product_name,))
        connection.commit()
        print("product deleted from cart.")
    else:
        print("product not found in cart.")
    cursor.close()
    connection.close()

#function to update quantity
def update_quantity():
    connection=create_connection()
    cursor=connection.cursor()
    product_name=input("enter the product name:")
    cursor.execute("""SELECT cart.product_quantity,stock.product_quantity
        FROM cart
        JOIN stock
        ON cart.product_name = stock.product_name
        WHERE cart.product_name = %s""",(product_name,))
    product=cursor.fetchone()
    if product:
        product_quantity=int(input("enter the quantity to update:"))
        if product_quantity>product[1]:
            print("no enough stock.")
        else:
            cursor.execute("update cart set product_quantity=%s where product_name=%s",(product_quantity,product_name))
            connection.commit()
            print("product quantity updated successfully.")
    else:
        print("no such product found in cart.")  
    cursor.close()
    connection.close() 


#function to calculate total
def calculate_total():
    connection=create_connection()
    cursor=connection.cursor()
    cursor.execute( """
        SELECT cart.product_name,
               cart.product_quantity,
               stock.price
        FROM cart
        JOIN stock
        ON cart.product_name = stock.product_name
        """
    )
    products = cursor.fetchall()
    total = 0
    for product in products:
        product_name = product[0]
        product_quantity = product[1]
        price = product[2]
        amount = product_quantity * price
        total = total + amount
    print("Total amount:", total)
    cursor.close()
    connection.close()
    return total

#function to apply discount
def apply_discount():
    connection=create_connection()
    cursor=connection.cursor()
    amount = calculate_total()
    if amount > 10000:
       print("You got 20% discount.")
       discount = amount * 20 / 100
       amount = amount - discount
       print("Final amount:", amount)
    else:
        print("No discount available,discount applicable only for amount greaterthan 10000")
        print("Final amount:", amount)
    cursor.close()
    connection.close()

# function to checkout

def checkout():
    connection=create_connection()
    cursor=connection.cursor()
    try:
        connection.start_transaction()
        cursor.execute("""
            SELECT cart.product_name,
                   cart.product_quantity,
                   stock.product_quantity,
                   stock.price
            FROM cart
            JOIN stock
            ON cart.product_name = stock.product_name
            """
        )
        products = cursor.fetchall()
        if not products:
            print("Cart is empty.")
            connection.rollback()
            return
        total=0
        for product in products:
            product_name = product[0]
            product_quantity = product[1]
            if product_quantity > product[2]:
                print("Not enough stock for", product_name)
                connection.rollback()
                return
            total=total+(product_quantity*product[3])
        if total > 1000:
            discount = total * 20 / 100
        else:
            discount = 0
        final_amount = total - discount
        for product in products:
            product_name = product[0]
            product_quantity = product[1]

            cursor.execute(
                """UPDATE stock
                SET product_quantity = product_quantity - %s
                WHERE product_name = %s""",
                (product_quantity, product_name)
            )
        cursor.execute("DELETE FROM cart")
        connection.commit()

        print("Checkout successful.")
        print("Total amount:", total)
        print("Discount:", discount)
        print("Final amount:", final_amount)
    except Exception as e:
        connection.rollback()
        print("Checkout failed:", e)
    cursor.close()
    connection.close() 
  

# main menu
while True:

    print("\n=========== ONLINE SHOPPING CART ==========")

    print("1. Add product to stock")
    print("2. Add product to cart")
    print("3. Delete product from cart")
    print("4. Update cart quantity")
    print("5. Calculate total")
    print("6. Apply discount")
    print("7. Checkout")
    print("8. Exit")
    print("=========================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_stock()

    elif choice == "2":
        add_to_cart()

    elif choice == "3":
        delete_product()

    elif choice == "4":
        update_quantity()

    elif choice == "5":
        calculate_total()

    elif choice == "6":
        apply_discount()

    elif choice == "7":
        checkout()

    elif choice == "8":
        print("Thank you.")
        break

    else:
        print("Invalid choice.")

            

           
