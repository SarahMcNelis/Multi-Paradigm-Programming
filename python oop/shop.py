# Multi-Paradigm Programming Project.
# This program is a simulation of a shop using python object orientated programming (OOP).
# Author: Sarah McNelis
# StudentID: G00398343


# IMPORT MODULES HERE
import csv


# PRODUCT CLASS
class Product:
    def __init__(self, name, price=0):
        self.name = name
        self.price = price

    # Print out details
    def __repr__(self):
        return f"{self.name} @ €{float(self.price)} each"


# PRODUCT STOCK CLASS
class ProductStock:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    # Return product name
    def name(self):
        return self.product.name

    # Return product price
    def prodPrice(self):
        return self.product.price

    # Return cost of product
    def cost(self):
        return (self.prodPrice() * self.quantity)

    # And print out
    def __repr__(self):
        return f'\nThe shop has {int(self.quantity)} of {self.product}\n'


# CUSTOMER CLASS
class Customer:
    def __init__(self, pathName):
        self.shoppingList = []
        # Allowing for option a and b in display menu
        if pathName == None:
            file_path = f"../customer.csv"
        else:
            file_path = f"../customers/{pathName}.csv"

        # Read in customer data 
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Seperate out name and budget
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            # Now loop to get wishlist
            for row in csv_reader:
                name = row[0]
                quantity = int(row[1])
                product = Product(name)
                prodStock = ProductStock(product, quantity)
                # And append to empty list
                self.shoppingList.append(prodStock)  

        return 

    # Calculate customer items cost
    def customer_cost(self, priceList):
        # For all products
        for p in priceList:
            # And for items shopping list
            for item in self.shoppingList:
                # If there is a match
                if (item.name() == p.name()):
                    # Retrieve the price from productStock class
                    item.product.price = p.prodPrice()

    # Calculate total item cost
    def cost_of_order(self):
        cost = 0 
        # Loop through shopping list and retrieve the cost
        for item in self.shoppingList:
            cost += item.cost()
            
        return cost

    # Update customer info
    def update_customer(self, pathName):
        # Allowing for option a or b in display menu
        if pathName == None:
            file_path = f"../customer.csv"
        else:         
            file_path = f"../customers/{pathName}.csv"
        # Open csv in write mode
        with open (file_path, 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            # First line
            update = (self.name, round(self.budget, 2))
            csv_writer.writerow(update)
            # Now update wishlist
            for item in self.shoppingList:
                newList = (item.product.name, int(item.quantity))
                csv_writer.writerow(newList)

    # Print info out
    def __repr__(self):
        # Customer name and budget
        print(f'\nCUSTOMER NAME: {self.name} \nCUSTOMER BUDGET: {self.budget}\n')
        print('---------------------------------------------')
        # Customer wishlist
        for item in self.shoppingList:
            #print(f"\nPRODUCT/PRICE: {item.product}")
            print(f'YOUR ORDER: {item.product.name} x {item.quantity}')
            cost = item.quantity * item.product.price
            print(f'\n{self.name} OWES €{round(cost, 2)} TO THE SHOP\n')
            print('---------------------------------------------')
            customerBill = round(self.cost_of_order(), 2)
            total = ""
            total += (f'\nTotal cost of {self.name}s shop will be €{customerBill}\n')   

        return total


# LIVE SHOP CLASS
class Live_shop:
    def __init__(customer, pathName):
        file_path = f'../customers/{pathName}.csv' 
        with open(file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            budget = float(input("Please enter your budget: €"))
            customer = (pathName, budget)
            csv_writer.writerow(customer)
            while True:
                items = input("\nWhat would you like to order? ")
                itemQuantity = input(f"\nHow many of {items} would you like to buy? ")              
                customer = (items, itemQuantity)
                csv_writer.writerow(customer)
                choice = input("\nPress enter to continue shopping or press 0 to exit: ")
                if choice == "0":
                    break
            
        csv_file.close()


# SHOP CLASS
class Shop:
    def __init__(self, file_path):
        self.prodStock = []       
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # Take out shop tote
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
        	# Loop to get stock and append to empty list
            for row in csv_reader:
                product = Product(row[0], float(row[1]))
                prods = ProductStock(product, float(row[2]))
                self.prodStock.append(prods)

    # Print shop tote and stock
    def __repr__(self):
        str = ""
        str += f'SHOP TOTE IS: €{float(round(self.cash, 2))}\n'
        str += '---------------------\n'
        print('SHOP STOCK:\n')
        # Loop to print stock
        for item in self.prodStock:         
            str += f"{item}\n"

        return str

    # Check stock
    def check_stock(shop, name):
        # Loop through every item in shops stock
        for item in shop.prodStock:
            # If a match return item
            if item.product.name == name:  
                return item

        return None
        
    # Process customer order
    def customer_check_out(self, customer):
        cash = float(self.cash)
        budget = float(customer.budget)
        start = budget
        total = 0 
        # Loop wishlist and check stock levels
        for item in customer.shoppingList:
            # Check if product in stock
            stockLevels = self.check_stock(item.product.name)
            
            if stockLevels == None:
                print(f'\nSorry {item.product.name} is out of stock')

            else:
                itemCost = item.quantity * stockLevels.product.price

                # Check if amount of products in stock
                if item.quantity <= stockLevels.quantity:                   
                    print(f'\nShop has {item.quantity} {item.product.name} which costs €{stockLevels.product.price}')

                    # Check customer budget
                    if budget >= itemCost:
                        # Update shop and customer budget
                        stockLevels.quantity -= item.quantity
                        cash += itemCost
                        budget -= itemCost
                        total += itemCost 
                    # If not enough in budget
                    elif budget < itemCost:
                        print(f'Sorry you do not have enough money to buy {item.product.name}')
                        continue    
                # If no stock                  
                else:
                    print('---------------------------------------------')
                    print(f'\nSorry the shop only has {stockLevels.quantity} of {item.product.name} and you want {item.quantity} of {item.product.name}.')
                    print(f'\nWe cannot fulfill your order of {item.product.name}.\n')
                    print('---------------------------------------------')

        # If all okay then deduct shopping bill from budget 
        if total < budget:
            print(f'\nYou owe the shop a total of €{float(round(total, 2))}\n')
            print('---------------------------------------------')
            print(f'\nYour budget was €{start}')
            newBudget = start - total
            newBudget = round(newBudget, 2)
            print(f'\nYour new budget is €{newBudget}\n')
            print('---------------------------------------------')
            print("Thanks for shopping at Sarah's Shop!")
            print('---------------------------------------------')   
        
        # Update cash values for shop and customer
        self.cash = cash
        customer.budget = newBudget

        return 

    # Update shop
    def update_shop(shop):
        # Open csv in write mode and update
        with open('../stock.csv', 'w', newline = "") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            cash = []
            roundCash = round(shop.cash, 2)
            cash.append(roundCash)
            csv_writer.writerow(cash)

            for item in shop.prodStock:
                new_stock = (item.product.name, item.product.price, int(item.quantity))
                csv_writer.writerow(new_stock)

    # Shop menu
    def display_menu(self):
        while True:
            print("\nWelcome to Sarah's Shop!\n")
            print("Please choose an option: ")
            print("------------------------------")
            print("(1) To read from customer.csv")
            print("(2) To use an existing account")
            print("(3) To enter the live shop ")
            print("(4) To see what's in stock ")
            print("(5) To exit the program")
            choice = input("Choice: ")
        
        # (1) READ CUSTOMER WITHOUT CHOICE 
            if choice == "1":
                print("--------------------------")
                print("\nREADING IN CUSTOMER.CSV\n")
                print("--------------------------") 
                pathName = None                
                cust = Customer(pathName)
                cust.customer_cost(self.prodStock)
                print(cust)
                self.customer_check_out(cust)
                self.update_shop()
                cust.update_customer(pathName)
                self.display_menu()

        # (2) FOR AN EXISTING ACCOUNT 
            if choice == "2":
                print("\nPlease choose an account: ")
                print("Conor")
                print("Jack")
                print("Peggy")
                print("Sarah")
                pathName = input("\nName: ")
                print("--------------------------")
                customers = ("Conor", "Jack", "Peggy", "Sarah")
                # Set path for dummy customers 
                if pathName in customers:                  
                    # Sending path to customer class
                    cust = Customer(pathName)
                    cust.customer_cost(self.prodStock)
                    print(cust)
                    self.customer_check_out(cust)
                    self.update_shop()
                    cust.update_customer(pathName)
                    self.display_menu()
                else:
                    print("Error: Please enter a valid account name\n")
                    self.display_menu()
        
        # (3) TO ENTER LIVE SHOP
            elif choice == "3":
                print("\nWelcome to Sarah's Live Shop\n")
                print("------------------------------\n")
                print("\nPlease choose an account: ")
                print("Conor")
                print("Jack")
                print("Peggy")
                print("Sarah")
                pathName = input("\nName: ")
                print("--------------------------")
                customers = ("Conor", "Jack", "Peggy", "Sarah")
                # Set path for dummy customers
                if pathName in customers:                 
                    Live_shop(pathName)
                    cust = Customer(pathName)
                    cust.customer_cost(self.prodStock)
                    print(cust)
                    self.customer_check_out(cust)
                    self.update_shop()
                    self.display_menu()
                else:
                    print("Error: Please enter a valid account name\n")
                    self.display_menu()

        # (4) TO SEE WHAT'S IN STOCK
            elif choice == "4":
                print("\n")   
                print(self)       
                self.display_menu()
        
        # (5) TO EXIT THE PROGRAM
            elif choice == "5":
                exit()
        
        # OTHERWISE KEEP PROMPTING
            else:
                print("Please choose an option")
                self.display_menu()


# MAIN FUNCTION
def main():
    print("\n***********************************")
    print("\nSHOPPING TIME WITH PYTHON OOP!!!\n")
    print("***********************************")
    s = Shop("../stock.csv")
    s.display_menu()


# CALL MAIN FUNCTION HERE
if __name__ == "__main__":
    main()