from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from venv import create
from xmlrpc.client import Server
import mysql.connector
from setuptools import Command
from cryptography.fernet import Fernet
import datetime

# Connecting to Database

pw = input("Enter root password: ")

mydb = mysql.connector.connect(
    host='Localhost',
    user='root',
    password=pw,
    port='3306',
    database='sys'
)
# Getting the original cursor
mycursor = mydb.cursor()


# Server View-----------------------------------------------------------------------------------------------
# page for the server view
class ServerView(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title("Server View")
        self.geometry("505x180")  
        self.info = employeeInfo

        # This is the button to create an order used by the server
        btnCreateOrder = Button(self, text="Create Order",
                        padx=50, pady=50, command=self.createOrder)
        btnCreateOrder.grid(row=0, column=0, sticky=E, padx=5, pady=5)

        # This is the button to view the orders used by the server
        btnViewOrder = Button(self, text="View Orders", padx=50, pady=50, command=self.viewOrder)
        btnViewOrder.grid(row=0, column=3, sticky=W, padx=5, pady=5)

        # This is the button to create a new customer
        btnAddCustomer = Button(self, text="Create New Customer", command=self.createNewCustomer)
        btnAddCustomer.grid(row=0, column=1, sticky=S, padx=5, pady=5)

        # Lets the current user log out to change employees
        btnLogout = Button(self, text="Log Out", command=self.logOut)
        btnLogout.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        # The current user who is logged in labale
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    # Creating an order button
    def createOrder(self):
        self.destroy()
        TableSelect(self.info)
        # print("New Order")

    # Viewing all the orders
    def viewOrder(self):
        self.destroy()
        ViewOrders(self.info)
        # print("View Order")

    # Creating a new customer button
    def createNewCustomer(self):
        self.destroy()
        NewCustomer(self.info)

    # Logging out a user
    def logOut(self):
        self.destroy()
        LoginView()

# Making a new window for selecting customers to a table/ Need to add querys here def submitTableInfo(self):
class TableSelect(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title("Table Select")
        self.geometry("470x140")
        self.info = employeeInfo
        # Makes the button that can cancel the page
        cancelButton = ttk.Button(self, text="Close", command=self.closeButton)
        cancelButton.grid(row=3, column=0, sticky=SE, padx=3, pady=3)

        # Makes drop down button for table number
        self.tableLabel = Label(self, text="Select the Table Number")
        self.tableLabel.grid(row=0, column=1, sticky=E, padx=3, pady=3)
        tableOptions = [" "]
        mycursor.execute('SELECT * FROM sys.nxtgen_table')
        tableInfo = mycursor.fetchall()
        for table in tableInfo:
            tableOptions.append("Table " + str(table[0]))
        self.tableDropDown = ttk.Combobox(self, value=tableOptions)
        self.tableDropDown.current(0)
        self.tableDropDown.grid(row=1, column=1, sticky=E, padx=3, pady=3)

        # Makes drop down button for Customer we are making an order for
        self.customerLabel = Label(self, text="Select the Customer Name")
        self.customerLabel.grid(row=0, column=2, sticky=E, padx=3, pady=3)
        customerOptions = [" "]
        mycursor.execute('SELECT * FROM sys.customer')
        customerInfo = mycursor.fetchall()
        for customer in customerInfo:
            customerOptions.append(str(customer[1]) + " " + str(customer[2]) + " (" + str(customer[0]) + ")")
        self.customerDropDown = ttk.Combobox(self, value=customerOptions)
        self.customerDropDown.current(0)
        self.customerDropDown.grid(row=1, column=2, sticky=E, padx=3, pady=3)

        # Making the submit button for getting the info
        self.button = ttk.Button(self, text='Submit')
        self.button['command'] = self.submitTableInfo
        self.button.grid(row=3, column=3, sticky=SW, padx=3, pady=3)

        # The current user who is logged in labale
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    # Button for submitting the information/ Need to add querys here def submitTableInfo(self):
    def submitTableInfo(self):
        table = self.tableDropDown.get()
        customer = self.customerDropDown.get()
        # If user puts nothing in table select print out alert
        if table == " ":
            messagebox.showwarning("showwarning", "No Table Selected")
        elif customer == " ":
            messagebox.showwarning("showwarning", "No Customer Selected")
        else:
            tableInfo = table.split(" ")
            tableID = tableInfo[1]
            custID = customer.split("(")[1].split(")")[0]
            args = (custID, self.info[0], tableID)
            mycursor.execute("UPDATE sys.nxtgen_table SET Customer_ID = %s, Employee_ID = %s WHERE Table_ID = %s", args)
            mydb.commit()
            self.destroy()
            MenuSelect(customer, self.info)

    # Close the window button
    def closeButton(self):
        self.destroy()
        ServerView(self.info)

# Choosing the items that the customer has ordered
class MenuSelect(tk.Tk):
    def __init__(self, customerName, employeeInfo):
        super().__init__()
        self.title("Menu Select")
        self.geometry("810x220")
        self.currCustomer = customerName
        self.info = employeeInfo
        # Labels for the different categories
        self.drinksLabel = Label(self, text="Drinks")
        self.drinksLabel.grid(row=0, column=0, padx=10, pady=3)

        self.alcoholLabel = Label(self, text="Alcohol")
        self.alcoholLabel.grid(row=0, column=1, padx=10, pady=3)

        self.appetizersLabel = Label(self, text="Appetizers")
        self.appetizersLabel.grid(row=0, column=2, padx=10, pady=3)

        self.entreesLabel = Label(self, text="Entrees")
        self.entreesLabel.grid(row=0, column=3, padx=10, pady=3)

        self.sidesLabel = Label(self, text="Sides")
        self.sidesLabel.grid(row=0, column=4, padx=10, pady=3)

        # Submit button
        self.custLabel = Label(self, text="Order for " + self.currCustomer)
        self.custLabel.grid(row=3, column=2, pady=5, sticky=N)
        self.submitButton = ttk.Button(self, text="Submit")
        self.submitButton['command'] = self.submitOrderInfo
        self.submitButton.grid(row=4, column=1, sticky=E)

        # Finish button
        self.finishButton = ttk.Button(self, text="Finish")
        self.finishButton['command'] = self.finishOrder
        self.finishButton.grid(row=4, column=3, sticky=W)

        # Setting null labels to fill in grid space
        self.nullLabel = Label(self, height=6)
        self.nullLabel.grid(row=2)

        # Populating the menu items
        mycursor.execute('SELECT * FROM sys.menu')
        menuItems = mycursor.fetchall()
        drinks = [""]
        alcohol = [""]
        appetizers = [""]
        entrees = [""]
        sides = [""]
        [drinks.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Drink"]
        [alcohol.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Alcohol"]
        [appetizers.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Appetizer"]
        [entrees.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Entree"]
        [sides.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Side"]

        # Use these lists to create our dropdowns
        self.drinksDown = ttk.Combobox(self, value=drinks)
        self.drinksDown.current(0)
        self.drinksDown.grid(row=1, column=0, padx=10, pady=3)

        self.alcoholDown = ttk.Combobox(self, value=alcohol)
        self.alcoholDown.current(0)
        self.alcoholDown.grid(row=1, column=1, padx=10, pady=3)

        self.appetizersDown = ttk.Combobox(self, value=appetizers)
        self.appetizersDown.current(0)
        self.appetizersDown.grid(row=1, column=2, padx=10, pady=3)

        self.entreesDown = ttk.Combobox(self, value=entrees)
        self.entreesDown.current(0)
        self.entreesDown.grid(row=1, column=3, padx=10, pady=3)

        self.sidesDown = ttk.Combobox(self, value=sides)
        self.sidesDown.current(0)
        self.sidesDown.grid(row=1, column=4, padx=10, pady=3)

        # The current user who is logged in labale
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    def submitOrderInfo(self):
        orderSub = False
        if (self.drinksDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            drinkID = str(self.drinksDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(drinkID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            orderSub = True
        if (self.alcoholDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            alcoholID = str(self.alcoholDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(alcoholID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            orderSub = True
        if (self.appetizersDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            appetizersID = str(self.appetizersDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(appetizersID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            orderSub = True
        if (self.entreesDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            entreesID = str(self.entreesDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(entreesID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            orderSub = True
        if (self.sidesDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            sidesID = str(self.sidesDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(sidesID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            orderSub = True
        if (orderSub):
            messagebox.showwarning("showinfo", "Order Submitted")
        else: 
            messagebox.showwarning("showinfo", "Choose at Least One Item")


    def finishOrder(self):
        self.destroy()
        ServerView(self.info)

# Making a new window for viewing all the orders
class ViewOrders(tk.Tk):
    def __init__(self, employee):
        super().__init__()
        self.title("Review Order")
        self.geometry("600x600")
        self.info = employee

        # To cancel the new customer creation
        cancelButton = ttk.Button(self, text="Close", command=self.closeButton)
        cancelButton.grid(row=0, column=4, sticky=E)

        # The current employees information being displayed
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

        # Lables for displaying information about the current employees orders
        self.orderLabel = Label(self, text="Current Orders For : " + self.info[1] + " " + self.info[2])
        self.orderLabel.grid(row=0, column=0, sticky=E, pady=5)

        self.custLabel = Label(self, text="Customer Name", font=('bold'))
        self.custLabel.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self.foodLabel = Label(self, text="Food Item Ordered", font=('bold'))
        self.foodLabel.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        self.priceLabel = Label(self, text="Price", font=('bold'))
        self.priceLabel.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        self.complLabel = Label(self, text="Status", font=('bold'))
        self.complLabel.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Making a null row for formating
        self.nullLabel = Label(self)
        self.nullLabel.grid(row=1, column=0)

        # Getting the actually information that will be displayed
        mycursor.execute('SELECT * FROM sys.nxtgen_order WHERE Employee_ID = ' + str(self.info[0]))
        orderInfo = mycursor.fetchall()
        i = 3
        for order in orderInfo:
            # print(order)
            self.foodID = order[1]
            self.customerID = order[0]
            self.completed = order[2]

            mycursor.execute('SELECT * FROM sys.menu WHERE Item_ID = ' + str(self.foodID))
            self.foodName = mycursor.fetchall()
            self.foodName1 = self.foodName[0][1]
            self.price = self.foodName[0][3]

            mycursor.execute('SELECT * FROM sys.customer WHERE Customer_ID = ' + str(self.customerID))
            self.customerName = mycursor.fetchall()
            self.customerName1 = self.customerName[0][1] + " " + self.customerName[0][2]

            # Shows the food items ordered by which customers
            self.cust = Label(self, text=self.customerName1)
            self.cust.grid(row=i, column=0, padx=5, pady=5, sticky=W)

            self.food = Label(self, text=self.foodName1)
            self.food.grid(row=i, column=1, padx=10, pady=5, sticky=W)

            self.price = Label(self, text="$" + str(self.price))
            self.price.grid(row=i, column=2, padx=10, pady=5, sticky=W)
            if (self.completed == 0):
                self.completed = Label(self, text="Pending")
                self.completed.grid(row=i, column=3, padx=10, pady=5, sticky=W)
            else:
                self.completed = Label(self, text="Completed")
                self.completed.grid(row=i, column=3, padx=10, pady=5, sticky=W)
            i += 1

    def closeButton(self):
        self.destroy()
        # if (self.)
        ServerView(self.info)

# Page for making a new customer
class NewCustomer(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        # Creating the new customer window
        self.title('Customer Info')
        self.geometry('410x140')
        self.info = employeeInfo

        # Creating the labels and the entries 
        self.FName = ttk.Entry(self)
        self.LName = ttk.Entry(self)
        self.Email = ttk.Entry(self)
        self.Notes = ttk.Entry(self)
        self.FName.grid(row=1, column=0, padx=5, pady=5)
        self.LName.grid(row=1, column=1, padx=5, pady=5)
        self.Email.grid(row=1, column=2, padx=5, pady=5)
        self.Notes.grid(row=3, column=1, padx=5, pady=5)
        self.firstLabel = Label(self, text="Enter First Name")
        self.firstLabel.grid(row=0, column=0, padx=5, pady=2)

        self.lastLabel = Label(self, text="Enter Last Name")
        self.lastLabel.grid(row=0, column=1, padx=5, pady=2)

        self.emailLabel = Label(self, text="Enter Email Name")
        self.emailLabel.grid(row=0, column=2, padx=5, pady=2)

        self.notesLabel = Label(self, text="Enter General Notes")
        self.notesLabel.grid(row=2, column=1, padx=5, pady=2)

        # Creating the submit button once information is entered
        self.button = ttk.Button(self, text='Submit')
        self.button['command'] = self.button_clicked
        self.button.grid(row=4, column=2, sticky=W)

        # To cancel the new customer creation
        cancelButton = ttk.Button(self, text="Close", command=self.closeButton)
        cancelButton.grid(row=4, column=0, sticky=E)

    # When information is entered this will submit it to the database
    def button_clicked(self):
        mycursor.execute('SELECT * FROM sys.customer')
        tableInfo = mycursor.fetchall()
        newID = 1 + len(tableInfo)

        # If customer first name is null, we require that they input a first name
        if self.FName.get() == "":
            messagebox.showwarning("showwarning", "Please Enter First Name")

        # If customer last name is null, we require that they input a last name
        elif self.LName.get() == "":
            messagebox.showwarning("showwarning", "Please Enter Last Name")

        # If customer does not want to give email and notes, make those null
        elif self.Email.get() == "" and self.Notes.get() == "":
            args = (newID, self.FName.get(), self.LName.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView(self.info)

        # If customer does not want to give notes, make it null
        elif self.Notes.get() == "":
            args = (newID, self.FName.get(), self.LName.get(), self.Email.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName, Email) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView(self.info)

        # If customer does not want to give email, make it null
        elif self.Email.get() == "":
            args = (newID, self.FName.get(), self.LName.get(), self.Notes.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName, General_Notes) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView(self.info)

        # If all values are entered we do a regular sql add with all information
        else:
            args = (newID, self.FName.get(), self.LName.get(), self.Email.get(), self.Notes.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName, Email, General_Notes) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView(self.info)

    # Close the window button
    def closeButton(self):
        self.destroy()
        ServerView(self.info)
#----------------------------------------------------------------------------------------------------------


# Cook View------------------------------------------------------------------------------------------------
# Page for cook view
class CookView(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title("Cook View")
        self.geometry("240x170")
        self.info = employeeInfo

        # This is the button to create an order used by the server
        btnViewOrder = Button(self, text="View Order",
                        padx=50, pady=50, command=self.viewOrder)
        btnViewOrder.grid(row=0, column=0, padx=5, pady=5)

        # Lets the current user log out to change employees
        btnLogout = Button(self, text="Log Out", command=self.logOut)
        btnLogout.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        # The current user who is logged in labale
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    def viewOrder(self):
        self.destroy()
        CookSelectCustomer(self.info)

    # Logging out a user
    def logOut(self):
        self.destroy()
        LoginView()

# Making a new window for selecting the customer
class CookSelectCustomer(tk.Tk):
    def __init__(self, employee):
        super().__init__()
        self.title("Cook Select Customer")
        self.geometry("180x180")
        self.info = employee
        # 
        self.customerLabel = Label(self, text="Select the Customer Name")
        self.customerLabel.grid(row=0, column=0, padx=15, pady=3)
        customerOptions = [" "]
        mycursor.execute('SELECT * FROM sys.customer')
        customerInfo = mycursor.fetchall()
        for customer in customerInfo:
            customerOptions.append(str(customer[1]) + " " + str(customer[2]) + " (" + str(customer[0]) + ")")
        self.customerDropDown = ttk.Combobox(self, value=customerOptions)
        self.customerDropDown.current(0)
        self.customerDropDown.grid(row=1, column=0, padx=15, pady=3)

        # Null label to make an extra row
        self.nullLabel = Label(self, height=2)
        self.nullLabel.grid(row=2, column=0)

        # Making the submit button for getting the info
        self.button = ttk.Button(self, text='Submit')
        self.button['command'] = self.submitCustomer
        self.button.grid(row=3, column=0, sticky=E, pady=3, padx=5)

        # Making the submit button for getting the info
        self.closebutton = ttk.Button(self, text='Close')
        self.closebutton['command'] = self.closeCustomer
        self.closebutton.grid(row=3, column=0, sticky=W, pady=3, padx=5)

    # Lets the cook choose which customer he wants to look at 
    def submitCustomer(self):
        customer = self.customerDropDown.get()
        # If user puts nothing in table select print out alert
        if customer == " ":
            messagebox.showwarning("showwarning", "No Customer Selected")
        else:
            customerInfo = customer.split(" ")
            customerFName, customerLName = customerInfo[0], customerInfo[1]
            # print(customerFName + " " + customerLName)
            self.destroy()
            CookViewOrders(customer, self.info)

    # Lets the user close out of this window
    def closeCustomer(self):
        self.destroy()
        CookView(self.info)

# Making a new view for the cook to view and complete orders
class CookViewOrders(tk.Tk):
    def __init__(self, customer, employee):
        super().__init__()
        self.title("Review Order")
        self.geometry("600x600")
        self.info = employee
        self.custInfo = customer

        # To cancel the new customer creation
        cancelButton = ttk.Button(self, text="Close", command=self.closeButton)
        cancelButton.grid(row=0, column=2, sticky=E)

        # To submit the customers order
        submitButton = ttk.Button(self, text="Mark Order Completed", command=self.submitOrder)
        submitButton.grid(row=0, column=3, sticky=E)

        # The current employees information being displayed
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

        # Lables for displaying information about the current employees orders
        self.orderLabel = Label(self, text="Current Orders For : " + self.info[1] + " " + self.info[2])
        self.orderLabel.grid(row=0, column=0, sticky=E, pady=5)

        self.custLabel = Label(self, text="Customer Name", font=('bold'))
        self.custLabel.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self.foodLabel = Label(self, text="Food Item Ordered", font=('bold'))
        self.foodLabel.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        self.priceLabel = Label(self, text="Price", font=('bold'))
        self.priceLabel.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        self.complLabel = Label(self, text="Status", font=('bold'))
        self.complLabel.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Making a null row for formating
        self.nullLabel = Label(self)
        self.nullLabel.grid(row=1, column=0)

        self.custID = self.custInfo.split("(")[1].split(")")[0]

        # Getting the actually information that will be displayed
        mycursor.execute('SELECT * FROM sys.nxtgen_order WHERE Customer_ID = ' + self.custID)
        orderInfo = mycursor.fetchall()
        i = 3
        for order in orderInfo:
            self.foodID = order[1]
            self.customerID = order[0]
            self.completed = order[2]

            mycursor.execute('SELECT * FROM sys.menu WHERE Item_ID = ' + str(self.foodID))
            self.foodName = mycursor.fetchall()
            self.foodName1 = self.foodName[0][1]
            self.price = self.foodName[0][3]

            mycursor.execute('SELECT * FROM sys.customer WHERE Customer_ID = ' + str(self.customerID))
            self.customerName = mycursor.fetchall()
            self.customerName1 = self.customerName[0][1] + " " + self.customerName[0][2]

            # Shows the food items ordered by which customers
            self.cust = Label(self, text=self.customerName1)
            self.cust.grid(row=i, column=0, padx=5, pady=5, sticky=W)

            self.food = Label(self, text=self.foodName1)
            self.food.grid(row=i, column=1, padx=10, pady=5, sticky=W)

            self.price = Label(self, text="$" + str(self.price))
            self.price.grid(row=i, column=2, padx=10, pady=5, sticky=W)
            if (self.completed == 0):
                self.completed = Label(self, text="Pending")
                self.completed.grid(row=i, column=3, padx=10, pady=5, sticky=W)
            else:
                self.completed = Label(self, text="Completed")
                self.completed.grid(row=i, column=3, padx=10, pady=5, sticky=W)
            i += 1

    def submitButton(self):
        self.destroy()
        # if (self.)
        CookView(self.info)

    def closeButton(self):
        self.destroy()
        # if (self.)
        CookView(self.info)

    def submitOrder(self):
        mycursor.execute("UPDATE sys.nxtgen_order SET Completed = 1 WHERE Customer_ID = " + str(self.custID))
        mydb.commit()
        self.destroy()
        CookView(self.info)
#----------------------------------------------------------------------------------------------------------


# Manager View------------------------------------------------------------------------------------------------
class ManagerView(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title("Manager View")
        self.geometry("515x200")
        self.info = employeeInfo

        # This is the button to create an order used by the server
        btndata = Button(self, text="Data Analytics",padx=50, pady=50, command=self.viewData)
        btndata.grid(row=0, column=0, sticky=E, padx=5, pady=5)

        # This is the button to view the orders used by the server
        btnViewOrder = Button(self, text="View Orders", padx=50, pady=50, command=self.viewOrder)
        btnViewOrder.grid(row=0, column=3, sticky=W, padx=5, pady=5)

        # This is the button to create a new customer
        btnAddCustomer = Button(self, text="Create New Employee", command=self.createNewEmployee)
        btnAddCustomer.grid(row=0, column=1, sticky=S, padx=5, pady=5)

        # Lets the current user log out to change employees
        btnLogout = Button(self, text="Log Out", command=self.logOut)
        btnLogout.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        # The current user who is logged in labale
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    def viewData(self):
        print("data")

    def viewOrder(self):
        self.destroy()
        ManagerSelectServer(self.info)

    def createNewEmployee(self):
        self.destroy()
        CreateNewEmployee(self.info)

    def logOut(self):
        self.destroy()
        LoginView()

class CreateNewEmployee(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title('New Employee Info')
        self.geometry('450x140')
        self.info = employeeInfo

        # Creating the labels and the entries 
        self.FName = ttk.Entry(self)
        self.LName = ttk.Entry(self)
        self.Wage = ttk.Entry(self)
        self.WageType = ttk.Entry(self)

        positionOptions = [" ", "Server", "Cook", "Manager"]
        self.positionDropDown = ttk.Combobox(self, value=positionOptions)
        self.positionDropDown.current(0)
        self.positionDropDown.grid(row=3, column=2, padx=5, pady=5)

        wageOptions = [" ", "Hourly", "Salary"]
        self.wageDropDown = ttk.Combobox(self, value=wageOptions)
        self.wageDropDown.current(0)
        self.wageDropDown.grid(row=3, column=0, padx=5, pady=5)

        self.FName.grid(row=1, column=0, padx=5, pady=5)
        self.LName.grid(row=1, column=1, padx=5, pady=5)
        self.Wage.grid(row=1, column=2, padx=5, pady=5)

        self.firstLabel = Label(self, text="Enter First Name")
        self.firstLabel.grid(row=0, column=0, padx=5, pady=2)

        self.lastLabel = Label(self, text="Enter Last Name")
        self.lastLabel.grid(row=0, column=1, padx=5, pady=2)

        self.wageLabel = Label(self, text="Wage")
        self.wageLabel.grid(row=0, column=2, padx=5, pady=2)

        self.typeLabel = Label(self, text="Wage Type")
        self.typeLabel.grid(row=2, column=0, padx=5, pady=2)

        self.positionLabel = Label(self, text="Job Position")
        self.positionLabel.grid(row=2, column=2, padx=5, pady=2)

        # Creating the submit button once information is entered
        self.button = ttk.Button(self, text='Submit')
        self.button['command'] = self.submitButton
        self.button.grid(row=4, column=2, sticky=W)

        # To cancel the new customer creation
        cancelButton = ttk.Button(self, text="Close", command=self.closeButton)
        cancelButton.grid(row=4, column=0, sticky=E)

    def closeButton(self):
        self.destroy()
        ManagerView(self.info)

    def submitButton(self):
        self.Key = b'l2ihTWOCdrskUed1cWfgMGQzwGOSD3EiKZ0IxWQGpzc='
        self.fernet = Fernet(self.Key)

        mycursor.execute('SELECT * FROM sys.employee')
        tableInfo = mycursor.fetchall()

        # If customer first name is null, we require that they input a first name
        if (self.FName.get() == "") or (self.LName.get() == "") or (self.Wage.get() == "") or (self.wageDropDown.get() == " ") or (self.positionDropDown.get() == " "):
            messagebox.showwarning("showwarning", "Please Enter All Fields")
        else:
            self.newID = 1 + len(tableInfo)
            self.date = datetime.datetime.utcnow()
            self.username = (self.FName.get() + self.LName.get()).lower()
            self.password = self.fernet.encrypt(str(self.username + "2022").encode())
            args = (self.newID, self.FName.get(), self.LName.get(), float(self.Wage.get()), self.wageDropDown.get(), self.date.strftime('%Y-%m-%d %H:%M:%S'), self.positionDropDown.get(), self.username, str(self.password.decode()))
            query = "INSERT INTO employee(Employee_ID, FName, LName, Wage, Wage_Unit, Date_Joined, Type, Username, Password) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ManagerView(self.info)

class ManagerSelectServer(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title("Select Server View")
        self.geometry("165x150")
        self.info = employeeInfo

        # Making the Label for the drop down
        self.serverLabel = Label(self, text="Select an Employee")
        self.serverLabel.grid(row=0, column=0, padx=10)

        # Making the Drop down to select an employee
        servers = [" "]
        mycursor.execute('SELECT * FROM sys.employee')
        serverInfo = mycursor.fetchall()
        for server in serverInfo:
            if (str(server[6]) == "Server"): 
                servers.append(str(server[1]) + " " + str(server[2]) + " (" + str(server[0]) + ")")
        self.serverDropDown = ttk.Combobox(self, value=servers)
        self.serverDropDown.current(0)
        self.serverDropDown.grid(row=1, column=0, padx=10, pady=10)

        # Making a null row for spacing
        self.nullLabel = Label(self)
        self.nullLabel.grid(row=2, pady=10)

        # Making a Close button
        self.closeButton = ttk.Button(self, text="Close", command=self.closeFun)
        self.closeButton.grid(row=3, column=0, sticky=W)

        # Making a submit button
        self.submitButton = ttk.Button(self, text="Submit", command=self.submitBtn)
        self.submitButton.grid(row=3, column=0, sticky=E)

    # The closing button
    def closeFun(self):
        self.destroy()
        ManagerView(self.info)

    def submitBtn(self):
        if (str(self.serverDropDown.get()) == " "):
            messagebox.showwarning("showwarning", "Please Select A Server")
        else:
            ManagerViewOrders(self.info, self.serverDropDown.get())
            self.destroy()

class ManagerViewOrders(tk.Tk):
    def __init__(self, managerInfo, serverInfo):
        super().__init__()
        self.title("Manager View Orders")
        self.geometry("600x600")
        self.info = managerInfo
        self.sInfo = serverInfo
        
        # Server Info Display
        self.serverInfo = Label(self, text="Current Orders For : " + str(self.sInfo))
        self.serverInfo.grid(row=0, column=0)

        # The current user who is logged in labale
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

        self.custLabel = Label(self, text="Customer Name", font=('bold'))
        self.custLabel.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self.foodLabel = Label(self, text="Food Item Ordered", font=('bold'))
        self.foodLabel.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        self.priceLabel = Label(self, text="Price", font=('bold'))
        self.priceLabel.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        self.complLabel = Label(self, text="Status", font=('bold'))
        self.complLabel.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # To cancel the new customer creation
        cancelButton = ttk.Button(self, text="Close", command=self.closeButton)
        cancelButton.grid(row=0, column=4, sticky=E)

        # Making a null row for formating
        self.nullLabel = Label(self)
        self.nullLabel.grid(row=1, column=0)

        # Getting the actually information that will be displayed
        self.serverID = self.sInfo.split("(")[1].split(")")[0]
        mycursor.execute('SELECT * FROM sys.nxtgen_order WHERE Employee_ID = ' + self.serverID)
        orderInfo = mycursor.fetchall()
        i = 3
        for order in orderInfo:
            self.foodID = order[1]
            self.customerID = order[0]
            self.completed = order[2]

            mycursor.execute('SELECT * FROM sys.menu WHERE Item_ID = ' + str(self.foodID))
            self.foodName = mycursor.fetchall()
            self.foodName1 = self.foodName[0][1]
            self.price = self.foodName[0][3]

            mycursor.execute('SELECT * FROM sys.customer WHERE Customer_ID = ' + str(self.customerID))
            self.customerName = mycursor.fetchall()
            self.customerName1 = self.customerName[0][1] + " " + self.customerName[0][2]

            # Shows the food items ordered by which customers
            self.cust = Label(self, text=self.customerName1)
            self.cust.grid(row=i, column=0, padx=5, pady=5, sticky=W)

            self.food = Label(self, text=self.foodName1)
            self.food.grid(row=i, column=1, padx=10, pady=5, sticky=W)

            self.price = Label(self, text="$" + str(self.price))
            self.price.grid(row=i, column=2, padx=10, pady=5, sticky=W)
            if (self.completed == 0):
                self.completed = Label(self, text="Pending")
                self.completed.grid(row=i, column=3, padx=10, pady=5, sticky=W)
            else:
                self.completed = Label(self, text="Completed")
                self.completed.grid(row=i, column=3, padx=10, pady=5, sticky=W)
            i += 1

    def closeButton(self):
        self.destroy()
        # if (self.)
        ManagerView(self.info)


# Making a new window for logging in 
class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login In")
        self.geometry("280x160")

        # Username entry and label box
        self.userLabel = Label(self, text="Username")
        self.userLabel.grid(row=0, column=1, sticky=N, pady=2)
        self.userName = ttk.Entry(self)
        self.userName.grid(row=1, column=1, pady=5)

        # Password entry and label box
        self.passLabel = Label(self, text="Password")
        self.passLabel.grid(row=2, column=1, sticky=N, pady=2)
        self.password = ttk.Entry(self, show="*")
        self.password.grid(row=3, column=1, pady=5)

        # Button that will login a user in, gives a warning if it is wrong
        self.loginBtn = ttk.Button(self, text='Login')
        self.loginBtn['command'] = self.loginUser
        self.loginBtn.grid(row=4, column=2, sticky=E, pady=5)

        # Button that will close the entire window 
        self.closeBtn = ttk.Button(self, text="Close", command=self.destroy)
        self.closeBtn.grid(row=4, column=0, sticky=E, pady=5)
        # self.encrptBtn = ttk.Button(self, text="encrypt", command=self.giveEncrptedPasswords).place(x=100, y=120)

    # This method is called to ensure users are in the database
    def loginUser(self):
        # Key for the encryption in bytes
        self.Key = b'l2ihTWOCdrskUed1cWfgMGQzwGOSD3EiKZ0IxWQGpzc='
        self.fernet = Fernet(self.Key)
        check = False
        # Want to check if any of the employees has this current username and password combination
        mycursor.execute('SELECT * FROM sys.employee')
        employees = mycursor.fetchall()
        for employee in employees:
            self.decMessage = self.fernet.decrypt(employee[8].encode()).decode()
            if ((self.password.get() == self.decMessage) and (self.userName.get() == employee[7])):
                # If it works and employee is a server, go to server view
                if (employee[6] == "Server"):
                    self.destroy()
                    ServerView(employee)
                # If it works and employee is a cook, go to cook view
                elif (employee[6] == "Cook"):
                    self.destroy()
                    CookView(employee)
                    # print("I am a cook")
                # If it works and employee is a manager, go to manager/admin view
                elif (employee[6] == "Manager"):
                    self.destroy()
                    ManagerView(employee)
                check = True
                break
        # If it goes through the entire loop without hitting anything, make warning
        if (not check):
            messagebox.showwarning("showwarning", "Incorrect Login! Please Try Again")

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()


