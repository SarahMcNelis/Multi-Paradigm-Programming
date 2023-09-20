# Multi-Paradigm Programming Project.
# This program is a simulation of a shop using python procedural programming.
# Author: Sarah McNelis
# StudentID: G00398343


# IMPORT MODULES HERE
import csv


# FUNCTION TO CREATE AND STOCK SHOP
def create_and_stock_shop():
    # Making shop a dict - set of key value pairs. Keys aren't indexes they're names.
    shop = {}
    # Open the csv
    with open ('..\stock.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        # Get shop tote out first
        first_row = next(csv_reader)
        shop["cash"] = float(first_row[0])
        # List to add products to
        shop["products"] = []
        # Loop to get stock
        for row in csv_reader:
            # Creating a map for products
            product = {}
            product["name"] = row[0]
            product["price"] = float(row[1])
            product["quantity"] = int(row[2])
            # Append to list above
            shop["products"].append(product)

    return shop


# FUNCTION TO CHECK STOCK LEVELS
def check_stock(shop, name):
        # Loop through every item in shops stock
        for product in shop["products"]:
            # If a match return the item
            if product["name"] == product["name"]:
                # if found return ProductStock
                return product

        return None


# FUNCTION TO CALCULATE PRODUCT PRICE
def customer_cost(shop, customer):
    # For all products
    for item in shop["products"]:
        # And for items shopping list
        for product in customer["products"]:
            # If there is a match
            if (product["name"] == item["name"]):
                # Retrieve the price from productStock class
                product["price"] = item["price"]

    return item["price"]


# FUCNTION TO READ CUSTOMER ORDERS
def read_customer_order(path):
    customer = {}
    file_path = f"../customers/{path}.csv"
    with open (file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        # Take out first row and ID rest
        first_row = next(csv_reader)   
        customer["name"] = first_row[0]
        customer["cash"] = float(first_row[1])
        customer["products"] = []    
        # Loop for customer order
        for row in csv_reader:
            product = {}
            product["name"] = row[0]
            product["quantity"] = int(row[1])
            # Apend to product list
            customer["products"].append(product)

    return customer


# FUCNTION TO READ CUSTOMER CSV
def read_customer_csv():
    customer = {}
    file_path = f"../customer.csv"
    with open (file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        # Take out first row and ID rest
        first_row = next(csv_reader)
        customer["name"] = first_row[0]
        customer["cash"] = float(first_row[1])
        customer["products"] = []       
        # Loop for order
        for row in csv_reader:
            product = {}
            product["name"] = row[0]
            product["quantity"] = int(row[1])
            # Apend to product list
            customer["products"].append(product)

    return customer


# METHOD TO PRINT CUSTOMER INFO. 
def print_customer(customer, shop):
    print(f'\nCUSTOMER NAME: {customer["name"]} \nCUSTOMER BUDGET: €{customer["cash"]}\n')
    print("------------------------------------------------")      
    # Loop for customer order
    for product in customer["products"]:
        print(f'YOUR ORDER: {product["name"]} x {product["quantity"]}')         
        # If in stock continue
        if check_stock(shop, product) != None:
            order = check_stock(shop, product) 
            # Creating vars for multiplication           
            prodQ = float((product["quantity"]))
            prodP = float(customer_cost(shop, customer))
            itemCost = prodQ * prodP
            print(f'\n{customer["name"]} OWES €{round(itemCost, 2)} TO THE SHOP\n')
            print('---------------------------------------------')

    return


# FUNCTION TO PRINT SHOP STOCK
def print_shop(shop):
    print("------------------------------------------------")
    print(f'\nSHOP TOTE IS: €{round(shop["cash"], 2)}\n')   
    print("------------------------------------------------")  
    print("SHOP STOCK:")
    print("------------------------------------------------")
   # Loop to print each product
    for product in shop["products"]:
        print(f'{product["quantity"]} x {product["name"]} @ {product["price"]} each')
        print("------------------------------------------------")


# FUNCTION FOR LIVE SHOP
def live_shop(path):
    file_path = f'../customers/{path}.csv'
    with open (file_path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        # Get user budget and write to csv
        budget = float(input("Please enter your budget: €"))
        c = (path, budget)
        csv_writer.writerow(c)
        # Get user order and write to csv
        while True:
            items = input("\nWhat would you like to order? ")  
            itemQuantity = input(f"\nHow many of {items} would you like to buy? ")
            c = (items, itemQuantity)
            csv_writer.writerow(c)
            choice = input("\nPress enter to continue shopping or press 0 to exit: ")
            # Allow to exit shop 
            if choice == "0":
                break
        
    csv_file.close()


# FUNCTION FOR CHECK OUT
def customer_check_out(customer, shop):
    # Set vars   
    cash = float(shop["cash"])
    budget = float(customer["cash"])
    start = budget
    total = 0
    # Loop through wishlist
    for item in customer["products"]:
        # Check if product is in stock
        stockLevels = check_stock(shop, item["name"])   

        if stockLevels == None:
            print('---------------------------------------------')
            print(f'\nSorry {product["name"]} is out of stock\n')         

        elif stockLevels != None:
            # Calculate cost 
            itemQuantity = item["quantity"]
            itemPrice = float(stockLevels["price"])
            itemCost = itemQuantity * itemPrice

            # Check if enough of that product in stock
            if item["quantity"] <= stockLevels["quantity"]:
                print('---------------------------------------------')
                print(f'\nShop has {item["quantity"]} {item["name"]} which costs €{stockLevels["price"]}')

                # Check the budget
                if budget >= itemCost:      
                    # Updates shop and customer
                    stockLevels["quantity"] -= item["quantity"]
                    cash += itemCost
                    budget -= itemCost
                    total += itemCost
                # If not enough budget
                elif budget < itemCost:
                    print(f'\nSorry you do not have enough money to buy {item["name"]}')
                    continue
            # If no stock
            else:
                print(f'\nSorry the shop only has {int(stockLevels["quantity"])} of {item["name"]} and you want {int(item["quantity"])} of {item["name"]}.')
                print(f'\nWe cannot fulfill your order of {item["name"]}.\n')

    # If all okay then deduct shopping bill from budget
    if total < budget:
        print('---------------------------------------------')
        print(f'\n{customer["name"]} owes the shop a total of €{float(round(total, 2))}\n')
        print('---------------------------------------------')
        print(f'\nYour budget was €{start}')
        newBudget = start - total
        newBudget = round(newBudget, 2)
        print(f'\nYour new budget is €{newBudget}\n')
        print('---------------------------------------------')
        print("Thanks for shopping at Sarah's Shop!")
        print('---------------------------------------------')  
    
    # Update cash values for shop and customer
    shop["cash"] = cash
    customer["cash"] = budget

    return


# FUNCTION TO UPDATE SHOP
def update_shop(shop):
    with open ('../stock.csv', 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        # Add new cash to csv
        cash = []
        roundedCash = round(shop["cash"], 2)
        cash.append(roundedCash)
        csv_writer.writerow(cash)
        # Loop to add new stock to csv
        for product in shop["products"]:
            new_stock = (product["name"], product["price"], product["quantity"])
            csv_writer.writerow(new_stock)


# FUNCTION TO UPDATE CUSTOMER
def update_customer(customer, path):
    file_path = f"../customers/{path}.csv"
    with open (file_path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        # Add new name and budget to csv
        update = (customer["name"], round(customer["cash"], 2))
        csv_writer.writerow(update)
        # Add new order to csv
        for product in customer["products"]:
            newList = (product["name"], product["quantity"])
            csv_writer.writerow(newList)


# FUNCTION TO UPDATE CUSTOMER CSV
def update_customer_csv(customer):
    file_path = f"../customer.csv"
    with open (file_path, 'w', newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ',')
        # Add new name and budget to csv
        update = (customer["name"], round(customer["cash"], 2))
        csv_writer.writerow(update)
        # Add new order to csv
        for product in customer["products"]:
            newList = (product["name"], product["quantity"])
            csv_writer.writerow(newList)


# MENU FUNCTION
def display_menu():
    # List of names
    customers = ("Conor", "Jack", "Peggy", "Sarah")
    # Continues until broken
    while True:
        print("\nWelcome to Sarah's Shop!\n")
        print("Please choose an option: ")
        print("------------------------------")
        print("(1): To read from customer.csv")
        print("(2): To use an existing account")
        print("(3): To enter the live shop ")
        print("(4): To see what's in stock ")
        print("(5): To exit the program")
        choice = input("Choice: ")
    
    # (1) READ CUSTOMER WITHOUT CHOICE
        if choice == "1": 
            print("--------------------------")
            print("\nREADING IN CUSTOMER.CSV\n")
            print("--------------------------")
            order = read_customer_csv()
            print_customer(order, shop)
            customer_check_out(order, shop)
            update_shop(shop) 
            update_customer_csv(order)

    # (2) FOR AN EXISTING ACCOUNT
        elif choice == "2":
            print("\nPlease choose an account: ")
            print("Conor")
            print("Jack")
            print("Peggy")
            print("Sarah")
            path = input("\nName: ")
            print("--------------------------")
            # If its one of customers proceed with functions below
            if path in customers:
                order = read_customer_order(path)
                print_customer(order, shop)
                customer_check_out(order, shop)
                update_shop(shop) 
                update_customer(order, path)
            else:
                print("Error: Please enter a valid account name\n")
                display_menu() 

    # (3) TO ENTER LIVE SHOP
        elif choice == "3":
            print("\nWelcome to Sarah's Live Shop\n")
            print("------------------------------\n")
            print("\nPlease choose an account: ")
            print("Conor")
            print("Jack")
            print("Peggy")
            print("Sarah")
            path = input("\nName: ")
            print("--------------------------")
            # If its one of customers proceed with functions below
            if path in customers:        
                live_shop(path)
                order= read_customer_order(path)
                print_customer(order, shop)           
                customer_check_out(order, shop)
                update_shop(shop)
            else:
                print("Error: Please enter a valid account name\n")              
                display_menu()

    # (4) TO SEE WHAT'S IN STOCK
        elif choice == "4":
            print("\n")
            print_shop(shop)
            display_menu()

    # (5) TO EXIT THE PROGRAM
        elif choice == "5":
            exit()
    
    # OTHERWISE KEEP PROMPTING
        else:
            print("Please choose an option")
            display_menu()


# MAIN FUNCTION
def main():
    print("\n****************************************************")
    print("\nSHOPPING TIME WITH PYTHON PROCEDURAL PROGRAMMING!!!\n")
    print("****************************************************")
    display_menu()


# CALLING MAIN FUNCTION
if __name__ == "__main__":
    shop = create_and_stock_shop()
    main()