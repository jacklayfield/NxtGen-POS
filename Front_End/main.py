from asyncio.windows_events import NULL
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from venv import create
from xmlrpc.client import Server
import mysql.connector
from setuptools import Command

# Connecting to Database
mydb = mysql.connector.connect(
    host='Localhost',
    user='root',
    password='Fode1234',
    port='3306',
    database='sys'
)
# Getting the original cursor
mycursor = mydb.cursor()

# Page for making a new customer
class NewCustomer(tk.Tk):
    def __init__(self):
        super().__init__()
        # Creating the new customer window
        self.title('Customer Info')
        self.geometry('500x200')

        # Creating the labels and the entries 
        self.FName = ttk.Entry(self)
        self.LName = ttk.Entry(self)
        self.Email = ttk.Entry(self)
        self.Notes = ttk.Entry(self)
        self.FName.place(x=10, y=20)
        self.LName.place(x=200, y=20)
        self.Email.place(x=370, y=20)
        self.Notes.place(x=200, y=75)
        Label(self, text="Enter First Name").place(x=10)
        Label(self, text="Enter Last Name").place(x=200)
        Label(self, text="Enter Email Name").place(x=370)
        Label(self, text="Enter General Notes").place(x=200, y=50)

        # Creating the submit button once information is entered
        self.button = ttk.Button(self, text='Submit')
        self.button['command'] = self.button_clicked
        self.button.place(x=220, y=150)

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
            ServerView()

        # If customer does not want to give notes, make it null
        elif self.Notes.get() == "":
            args = (newID, self.FName.get(), self.LName.get(), self.Email.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName, Email) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView()

        # If customer does not want to give email, make it null
        elif self.Email.get() == "":
            args = (newID, self.FName.get(), self.LName.get(), self.Notes.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName, General_Notes) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView()

        # If all values are entered we do a regular sql add with all information
        else:
            args = (newID, self.FName.get(), self.LName.get(), self.Email.get(), self.Notes.get())
            query = "INSERT INTO customer(Customer_ID, FName, LName, Email, General_Notes) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
            self.destroy()
            ServerView()

# page for the server view
class ServerView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Server View")
        self.geometry("500x200")  

        # This is the button to create an order used by the server
        btnCreateOrder = Button(self, text="Create Order",
                        padx=50, pady=50, command=self.createOrder)
        btnCreateOrder.place(x=0, y=0)

        # This is the button to view the orders used by the server
        btnViewOrder = Button(self, text="View Order", padx=50,
                            pady=50, command=self.viewOrder)
        btnViewOrder.place(x=335, y=0)

        # This is the button to create a new customer
        btnAddCustomer = Button(
            self, text="Create New Customer", command=self.createNewCustomer)
        btnAddCustomer.place(x=190, y=100)

    # Creating an order button
    def createOrder(self):
        self.destroy()
        tablesel = TableSelect()
        tablesel.mainloop()
        print("New Order")

    def viewOrder(self):
        print("View Order")

    # Creating a new customer button
    def createNewCustomer(self):
        self.destroy()
        cust = NewCustomer()
        cust.mainloop()
        print("Create New Customer")

# Making a new window for selecting customers to a table
class TableSelect(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Table Select")
        self.geometry("500x200")

        # Makes the button that can cancel the page
        cancelButton = Button(self, text="Close",
                          command=self.closeButton)
        cancelButton.place(x=5, y=170)

        # Makes drop down button for table number
        Label(self, text="Select the Table Number").place(x=0)
        tableOptions = [" "]
        mycursor.execute('SELECT * FROM sys.nxtgen_table')
        tableInfo = mycursor.fetchall()
        for table in tableInfo:
            tableOptions.append("Table " + str(table[0]))
        self.tableDropDown = ttk.Combobox(self, value=tableOptions)
        self.tableDropDown.current(0)
        self.tableDropDown.place(x=0, y=20)

        # Makes drop down button for Customer we are making an order for
        Label(self, text="Select the Customer Name").place(x=160)
        customerOptions = [" "]
        mycursor.execute('SELECT * FROM sys.customer')
        customerInfo = mycursor.fetchall()
        for customer in customerInfo:
            customerOptions.append(str(customer[1]) + " " + str(customer[2]))
        self.customerDropDown = ttk.Combobox(self, value=customerOptions)
        self.customerDropDown.current(0)
        # self.customerDropDown.bind("<<ComboboxSelected>>", self.selectedTable)
        self.customerDropDown.place(x=160, y=20)

        # Making the submit button for getting the info
        self.button = ttk.Button(self, text='Submit')
        self.button['command'] = self.submitTableInfo
        self.button.place(x=220, y=150)

    # Button for submitting the information
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
            customerInfo = customer.split(" ")
            customerFName, customerLName = customerInfo[0], customerInfo[1]
            print(tableID + " " + customerFName + " " + customerLName)
            self.destroy()
            MenuSelect(customer)

    # Close the window button
    def closeButton(self):
        self.destroy()
        ServerView()

# Choosing the items that the customer has ordered
class MenuSelect(tk.Tk):
    def __init__(self, customerName):
        super().__init__()
        self.title("Menu Select")
        self.geometry("1000x200")
        self.currCustomer = customerName

        # Labels for the different categories
        Label(self, text="Drinks").place(x=5)
        Label(self, text="Alcohol").place(x=200)
        Label(self, text="Appetizers").place(x=400)
        Label(self, text="Entrees").place(x=600)
        Label(self, text="Sides").place(x=800)

        # Submit button
        Label(self, text="Order for " + self.currCustomer).place(x=445, y=150)
        self.submitButton = ttk.Button(self, text="Submit")
        self.submitButton['command'] = self.submitOrderInfo
        self.submitButton.place(x=430, y=170)

        # Finish button
        self.finishButton = ttk.Button(self, text="Finish")
        self.finishButton['command'] = self.finishOrder
        self.finishButton.place(x=520, y=170)

        # Populating the menu items
        mycursor.execute('SELECT * FROM sys.menu')
        menuItems = mycursor.fetchall()
        drinks = [""]
        alcohol = [""]
        appetizers = [""]
        entrees = [""]
        sides = [""]
        [drinks.append((item[1], item[3])) for item in menuItems if item[2] == "Drink"]
        [alcohol.append((item[1], item[3])) for item in menuItems if item[2] == "Alcohol"]
        [appetizers.append((item[1], item[3])) for item in menuItems if item[2] == "Appetizer"]
        [entrees.append((item[1], item[3])) for item in menuItems if item[2] == "Entree"]
        [sides.append((item[1], item[3])) for item in menuItems if item[2] == "Side"]

        # Use these lists to create our dropdowns
        self.drinksDown = ttk.Combobox(self, value=drinks)
        self.drinksDown.current(0)
        self.drinksDown.place(x=5, y=20)

        self.alcoholDown = ttk.Combobox(self, value=alcohol)
        self.alcoholDown.current(0)
        self.alcoholDown.place(x=200, y=20)

        self.appetizersDown = ttk.Combobox(self, value=appetizers)
        self.appetizersDown.current(0)
        self.appetizersDown.place(x=400, y=20)

        self.entreesDown = ttk.Combobox(self, value=entrees)
        self.entreesDown.current(0)
        self.entreesDown.place(x=600, y=20)

        self.sidesDown = ttk.Combobox(self, value=sides)
        self.sidesDown.current(0)
        self.sidesDown.place(x=800, y=20)

    def submitOrderInfo(self):
        print("Customer " + self.currCustomer + " ordered:")
        print(self.drinksDown.get())
        print(self.alcoholDown.get())
        print(self.appetizersDown.get())
        print(self.entreesDown.get())
        print(self.sidesDown.get())

    def finishOrder(self):
        self.destroy()
        ReviewOrder(self.currCustomer)

class ReviewOrder(tk.Tk):
    def __init__(self, customerName):
        super().__init__()
        self.title("Review Order")
        self.geometry("500x200")


if __name__ == "__main__":
    app = ServerView()
    app.mainloop()


