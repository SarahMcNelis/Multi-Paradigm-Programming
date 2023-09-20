// Multi-Paradigm Programming Project.
// This program is a simulation of a shop using c procedural programming. 
// Author: Sarah McNelis
// StudentID: G00398343


// INCLUDE THE FOLLOWING C LIBRARIES
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stddef.h>
#include <errno.h>


// Function for getline as suggested by Dominic. 
// Found here: <https://dev.w3.org/libwww/Library/src/vms/getline.c>
int getline(char **lineptr, size_t *n, FILE *stream){
static char line[256];
char *ptr;
unsigned int len;

   if (lineptr == NULL || n == NULL){
      errno = EINVAL;
      return -1;
   }
   if (ferror (stream))
      return -1;
  
   if (feof(stream))
      return -1;
     
   fgets(line,256,stream);

   ptr = strchr(line,'\n');   
   if (ptr)
      *ptr = '\0';

   len = strlen(line);
   
   if ((len+1) < 256){
      ptr = realloc(*lineptr, 256);
      if (ptr == NULL)
         return(-1);
      *lineptr = ptr;
      *n = 256;
   }
   strcpy(*lineptr,line); 
   return(len);
}


// PRODUCT STRUCT
struct Product {
	char* name;
	double price;
};


// PRODUCTSTOCK STRUCT
struct ProductStock {
	struct Product product;
	int quantity;
};


// SHOP STRUCT
struct Shop {
	double cash;
	struct ProductStock stock[20];
	// index to keep track of value
	int index;
};


// CUSTOMER STRUCT
struct Customer {
	char* name;
	double budget;
	struct ProductStock shoppingList[10];
	// index to keep track of value
	int index;
};


// PRINT PRODUCT INFO
void printProduct(struct Product p){
	printf("\n%s @ %.2f euro each\n", p.name, p.price);
	printf("\n---------------------------------------------\n");
}

// PRINT CUSTOMER FUNCTION
void printCustomer(struct Customer* c, struct Shop* s){
	printf("\nCUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f euro\n", c->name, c->budget);
	printf("\n---------------------------------------------\n");
	
	// For floats
	double sum = 0;
	
	// Loop through wishlist
	for (int i=0; i<c->index-1; i++){
		
		// For storing integar
		short checkStock = 0;
		
		// Create and copy products to the list
		char *list = malloc(sizeof(char) * 30);
		strcpy(list, c->shoppingList[i].product.name);	
		printf("\nYOUR ORDER:  %s x %d\n", c->shoppingList[i].product.name, c->shoppingList[i].quantity);
		
		// Loop through shop stock
		for (int j=0; j < s->index-1; j++){			
			char *shop = malloc(sizeof(char) * 30);
			strcpy(shop, s->stock[j].product.name);
			
			// Check if in stock
			if (strstr(list, shop) != NULL){			
				checkStock = 1;
				// Get product price
				double price = s->stock[j].product.price;
				// Cost to customer
				double cost = c->shoppingList[i].quantity * s->stock[j].product.price;
				printf("\n%s OWES %.2f euro TO THE SHOP\n", c->name, cost);
				printf("\n---------------------------------------------\n");
			}
		}
	}
}


// PRINT SHOP FUNCTION
void printShop(struct Shop s){
	printf("\nSHOP TOTE IS: %.2f euro\n", s.cash);
	printf("\n------------------------------\n");
	printf("\nSHOP STOCK:\n\n");

	// Loop to print shop stock
	for (int i=0; i<s.index; i++)
	{		
		printProduct(s.stock[i].product);
	}
}


// CREATE AND STOCK SHOP FUNCTION
struct Shop createAndStockShop(){
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

	// Open csv
    fp = fopen("../stock.csv", "r");

	// Exit if doesn't exist
    if (fp == NULL)
        exit(EXIT_FAILURE);

	// Get shop cash first
	read = getline(&line, &len, fp);
	float cash = atof(line);
	
	// Give that cash to shop 
	struct Shop shop = {cash};

    while ((read = getline(&line, &len, fp)) != -1) {
		// pointer to name and break the line on the comma
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");

		// Convert quantity into int
		int quantity = atoi(q);
		// Convert price into float 
		double price = atof(p);

		// Making a string copy as info is being overwritten
		char *name = malloc(sizeof(char) * 50);
		strcpy(name, n);

		// Adding items via structs 
		struct Product product = {name, price};
		struct ProductStock stockItem = {product, quantity};

		// Add stock to shop
		shop.stock[shop.index++] = stockItem;
    }	
	return shop;
}


// FUNCTION TO READ CUSTOMER ORDER
struct Customer readCustomerOrder(char* path)
{
	FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

	fp = fopen(path, "r");
	
	if (fp == NULL)
		exit(EXIT_FAILURE);
	
	// Get firstline name and budget
	read = getline(&line, &len, fp);
	char * n = strtok(line, ",");
	char * b = strtok(NULL, ",");
	char * name = malloc(sizeof(char) * 50);
	strcpy(name, n);
	
	double budget = atof(b);
	
	// Adding items via structs
	struct Customer order = {name, budget};
		
	// Get customer wishlist
	while ((read = getline(&line, &len, fp)) != -1) {	
			char * n = strtok(line, ",");
			char * q = strtok(NULL, ",");
			char * name = malloc(sizeof(char) * 50);
			strcpy(name, n);
			
			int quantity = atoi(q);
			
			// Adding items via structs
			struct Product product = { name };
			struct ProductStock customerItem = { product, quantity };
			// Add order to shopping list
			order.shoppingList[order.index++] = customerItem;
	}
	
	return order;
}

// CUSTOMER CHECK OUT FUNCTION
struct Shop customerCheckOut(struct Customer* c, struct Shop* s){
	
	double total = 0;
	
	// Loop through wishlist
	for (int i=0; i<c->index-1; i++){
		
		short checkStock = 0;
		char *list = malloc(sizeof(char) * 30);
		strcpy(list, c->shoppingList[i].product.name);
		
		// Loop through shop stock
		for (int j=0; j < s->index-1; j++){
			
			char *shop = malloc(sizeof(char) * 30);
			strcpy(shop, s->stock[j].product.name);
			
			// Check if in stock
			if (strstr(list, shop) != NULL){
				
				checkStock = 1;
				
				// Check quanitiy of item
				int orderAmt = c->shoppingList[i].quantity;
				int shopAmt = s->stock[j].quantity;
				double price = s->stock[j].product.price;
				
				// If in stock
				if (orderAmt <= shopAmt) {			
					printf("\n---------------------------------------------\n");
					printf("\nShop has %i %s which costs %.2f euro each\n", shopAmt, shop, price);	
					// Calculate total cost
					double totalPrice = 0;
					totalPrice += (orderAmt * price);
					
					// And check budget
					if (c->budget > totalPrice){				
						s->stock[j].quantity -= orderAmt;
						s->cash += (s->stock[j].product.price * orderAmt);
						total += (orderAmt * price);
					}
					// If budget not okay
					else if (c->budget < totalPrice){					
						printf("\nSorry you do not have enough money to buy %s\n", list);
						continue;
					}				
				}
							
				// If not in stock
				else {
					printf("\n---------------------------------------------\n");
					printf("\nSorry the shop only has %i of %s and you want %i of %s.\n", shopAmt, list, orderAmt, list);
					printf("\nWe cannot fulfill your order of %s.\n", list);
					
				}
			}
			
		}
	}
		// If all okay then deduct shopping bill from budget
		if (total < c->budget){	
			printf("\n---------------------------------------------\n");
			printf("\n%s owes the shop a total of %.2f euro\n", c->name, total);
			printf("\n---------------------------------------------\n");
			printf("\nYour budget was %.2f euro\n", c->budget);
			printf("\nYour new budget is %.2f euro\n", c->budget - total);
			printf("\n---------------------------------------------\n");
			printf("\nThanks for shopping at Sarah's Shop!\n");
			printf("\n---------------------------------------------\n");		
		}
		
		c->budget - total;
	
	return *s;
}


// LIVE SHOP FUNCTION
void liveShop(struct Shop s){
	
	struct Shop shop = createAndStockShop();
	
	char* path = (char*) malloc(10 * sizeof(char));
	char* custName = (char*) malloc(10 * sizeof(char));
	// Using name to open csv for live shop
	printf("\nName: ");
	scanf("%s", &custName);
	printf("--------------------------");
	
	// Set path
	sprintf(path, "../customers/%s.csv", &custName);
	
	FILE *fpw;	
	fpw = fopen(path, "w");
	
	if (fpw == NULL)
		exit(EXIT_FAILURE);
	
	// Set input char
	char* custBudget = (char*) malloc(10 * sizeof(char));
	printf("\nPlease enter your budget: ");
	scanf("%s", &custBudget);
	
	// Wrtie to file
	fprintf(fpw, "%s, %s\n", &custName, &custBudget);
			

	int shopping = 1;	
	char * prodName = (char*) malloc(10 * sizeof(char));
	char * prodQuantity = (char*) malloc(10 * sizeof(char));



		// Keep prompting until 0 is pressed
		while (shopping == 1) {
			// Get items
			printf("\nWhat would you like to order? ");
			scanf("%s", &prodName);
			// Get quantity
			printf("\nHow many of %s would you like to buy? ", &prodName);
			scanf("%s", &prodQuantity);
			// Write to csv
			fprintf(fpw, "%s, %s\n", &prodName, &prodQuantity);
			
			printf("\nPress 1 to continue or press 0 to exit: ");
			scanf("%d", &shopping);   
			
			// Exit
			if (shopping == 0) {
				// Close csv and call 3 functions to complete order
				fclose(fpw);
				printf("\n---------------------------------------------\n");											
				struct Customer customerLiveOrder = readCustomerOrder(path);
				printCustomer(&customerLiveOrder, &shop);
				customerCheckOut(&customerLiveOrder, &shop);
				}
			}
}


// UPDATE SHOP FUNCTION
void updateShop(struct Shop s){
	FILE * fp;
	char *filename = "../stock.csv";
	fp = fopen(filename, "w+");
	// Allow error
	if (fp == NULL){
		exit(EXIT_FAILURE);
	}
	
	// Write new shop cash to csv
	fprintf(fp, "%.2f\n", s.cash);
	
	// Loop to update stock
	for (int i=0; i<s.index-1; i++){
		fprintf(fp, "%s,%.2f,%i\n", s.stock[i].product.name, s.stock[i].product.price, s.stock[i].quantity);
	}
	// Close and return
	fclose(fp);
	return;
}


// DISPLAY MENU FUNCTION
void displayMenu(){
	
	struct Shop shop = createAndStockShop();
	int choice = -1;

	// While true
	while (choice !=0){
		fflush(stdin);
		printf("\nWelcome to Sarah's Shop!\n");
		printf("\nPlease choose an option: ");
		printf("\n------------------------------");
		printf("\n(1) To read from customer.csv");
		printf("\n(2) To use an existing account");
		printf("\n(3) To enter the live shop ");
		printf("\n(4) To see what's in stock ");
		printf("\n(5) To exit the program\n");
		printf("\nChoice: ");
		scanf("%d", &choice);
		printf("\n------------------------------\n");
	
	// (1) READ CUSTOMER WITHOUT CHOICE
		if (choice == 1){	
			printf("\n--------------------------\n");
            printf("\nREADING IN CUSTOMER.CSV\n");
            printf("\n--------------------------\n");
			//Assign the path 	
			char* path = (char*) malloc(10 * sizeof(char));		
			sprintf(path, "../customer.csv");
			//Call functions
			struct Customer order = readCustomerOrder(path);
			printCustomer(&order, &shop);
			customerCheckOut(&order, &shop);
			updateShop(shop);
		} 
			
	// (2) FOR AN EXISTING ACCOUNT
		else if (choice == 2){
            printf("\nPlease choose an account: ");
            printf("\nConor");
            printf("\nJack");
            printf("\nPeggy");
            printf("\nSarah\n");
			// Set chars for user input
			char* path = (char*) malloc(10 * sizeof(char));
			char* custName = (char*) malloc(10 * sizeof(char));
			// Get user input for path
			printf("\nName: ");					
            scanf(" %s", &custName);
            printf("\n--------------------------\n");
			// Now assign path
			sprintf(path, "../customers/%s.csv", &custName);
			//Call functions
			struct Customer order = readCustomerOrder(path);
			printCustomer(&order, &shop);
			customerCheckOut(&order, &shop);
			updateShop(shop);
		}
		
	// (3) TO ENTER LIVE SHOP
		else if (choice == 3){
			printf("\nWelcome to Sarah's Live Shop");
			printf("\n------------------------------");
			printf("\nPlease choose an account: ");
			printf("\nConor");
			printf("\nJack");
			printf("\nPeggy");
			printf("\nSarah\n");
			// Call functions
			liveShop(shop);
			updateShop(shop);
		}
		
	// (4) TO SEE WHAT'S IN STOCK
		else if (choice == 4){
			printShop(shop);
		}
	
	// (5) TO EXIT THE PROGRAM
		else if (choice == 5){
			break;
		}	
	}
}


// MAIN METHOD FUNCTION
int main(void) 
{
	printf("\n**************************************************\n");
    printf("\nSHOPPING TIME WITH C PROCEDURAL PROGRAMMING!!!\n");
    printf("\n**************************************************\n");
	struct Shop shop = createAndStockShop();
	displayMenu();

    return 0;
}