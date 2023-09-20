# Multi-Paradigm-Programming

This repository contains a project of a shop stimulation using 3 scripts. 

C using strutcs

Python using dictionaries (procedural)

Python object orientated Programming.

Each of the 3 programmes should display the same/similar interactive simulation of a shop.


Spec:
This Project is building on the shop program which I developed in the video series. You are tasked to add additional
functionality:
Functionality
• The shop CSV should hold the initial cash value for the shop.
• Read in customer orders from a CSV file.
– That file should include all the products they want and the quantity.
– It should also include their name and budget.
• The shop must be able to process the orders of the customer.
– Update the cash in the shop based on money received.
∗ It is important that the state of the shop be consistent.
∗ You should create customer test files (CSVs) which cannot be completed by the shop e.g. customer wants 400
loaves of bread but the shop only has 20, or the customer wants 2 cans of coke but can only afford 1.
∗ If these files don’t exist penalties will be applied.
– Know whether or not the shop can fill an order.
∗ Thrown an appropriate error.
• Operate in a live mode, where the user can enter a product by name, specify a quantity, and pay for it. The user should
be able to buy many products in this way