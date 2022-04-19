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

        # To cancel the new customer creation
        cancelButton = ttk.Button(self, text="Close",
                          command=self.closeButton)
        cancelButton.place(x=5, y=170)

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

    # Close the window button
    def closeButton(self):
        self.destroy()
        ServerView()

# page for the server view
class ServerView(tk.Tk):
    def __init__(self, serverInfo):
        super().__init__()
        self.title("Server View")
        self.geometry("500x200")  
        self.info = serverInfo

        # This is the button to create an order used by the server
        btnCreateOrder = Button(self, text="Create Order",
                        padx=50, pady=50, command=self.createOrder)
        btnCreateOrder.place(x=10, y=0)

        # This is the button to view the orders used by the server
        btnViewOrder = Button(self, text="View Orders", padx=50,
                            pady=50, command=self.viewOrder)
        btnViewOrder.place(x=325, y=0)

        # This is the button to create a new customer
        btnAddCustomer = Button(
            self, text="Create New Customer", command=self.createNewCustomer)
        btnAddCustomer.place(x=190, y=100)

        btnLogout = Button(self, text="Log Out", command=self.logOut)
        btnLogout.place(x=20, y=160)
        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        # self.loginInfo.place(y=150)
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    # Creating an order button
    def createOrder(self):
        self.destroy()
        TableSelect(self.info)
        # print("New Order")

    def viewOrder(self):
        self.destroy()
        ViewOrders(self.info)
        # print("View Order")

    # Creating a new customer button
    def createNewCustomer(self):
        self.destroy()
        NewCustomer()
        # print("Create New Customer")

    def logOut(self):
        self.destroy()
        LoginView()

# Making a new window for selecting customers to a table
class TableSelect(tk.Tk):
    def __init__(self, employeeInfo):
        super().__init__()
        self.title("Table Select")
        self.geometry("500x200")
        self.info = employeeInfo
        # Makes the button that can cancel the page
        cancelButton = ttk.Button(self, text="Close",
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
            customerOptions.append(str(customer[1]) + " " + str(customer[2]) + " (" + str(customer[0]) + ")")
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
            MenuSelect(customer, self.info)

    # Close the window button
    def closeButton(self):
        self.destroy()
        ServerView()

# Choosing the items that the customer has ordered
class MenuSelect(tk.Tk):
    def __init__(self, customerName, employeeInfo):
        super().__init__()
        self.title("Menu Select")
        self.geometry("1000x200")
        self.currCustomer = customerName
        self.info = employeeInfo
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
        [drinks.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Drink"]
        [alcohol.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Alcohol"]
        [appetizers.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Appetizer"]
        [entrees.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Entree"]
        [sides.append(str(item[1]) + " " + str(item[3]) + " (" + str(item[0]) + ")") for item in menuItems if item[2] == "Side"]

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
        if (self.drinksDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            drinkID = str(self.drinksDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(drinkID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
        if (self.alcoholDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            alcoholID = str(self.alcoholDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(alcoholID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
        if (self.appetizersDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            appetizersID = str(self.appetizersDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(appetizersID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
        if (self.entreesDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            entreesID = str(self.entreesDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(entreesID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
        if (self.sidesDown.get() != ""):
            custID = self.currCustomer.split("(")[1].split(")")[0]
            sidesID = str(self.sidesDown.get()).split("(")[1].split(")")[0]
            args = (int(custID), int(sidesID), 0, int(self.info[0]))
            query = "INSERT INTO nxtgen_order(Customer_ID, Item_ID, Completed, Employee_ID) VALUES" + str(args)
            mycursor.execute(query)
            mydb.commit()
        messagebox.showwarning("showinfo", "OrderSubmitted")

    def finishOrder(self):
        self.destroy()
        ServerView(self.info)
        # ReviewOrder(self.currCustomer)

class ViewOrders(tk.Tk):
    def __init__(self, employee):
        super().__init__()
        self.title("Review Order")
        self.geometry("500x600")
        self.info = employee

        self.loginInfo = Label(self, text="Logged in as " + self.info[1] + " " + self.info[2] + " (" + self.info[6] + ")")
        self.loginInfo.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

        Label(self, text="Current Orders For: " + self.info[1] + " " + self.info[2]).place(x=0, y=0)
        Label(self, text="Customer Name").place(x=30, y=30)
        Label(self, text="Food Item Ordered").place(x=150, y=30)
        Label(self, text="Price").place(x=280, y=30)
        Label(self, text="Completed").place(x=350, y=30)

        mycursor.execute('SELECT * FROM sys.nxtgen_order WHERE Employee_ID = ' + str(self.info[0]))
        orderInfo = mycursor.fetchall()
        for order in orderInfo:
            self.foodID = order[1]
            self.customerID = order[3]
            self.completed = order[2]

            mycursor.execute('SELECT * FROM sys.menu WHERE Item_ID = ' + str(self.foodID))
            self.foodName = mycursor.fetchall()
            self.foodName1 = self.foodName[0][1]
            print(self.foodName1)

            mycursor.execute('SELECT * FROM sys.customer WHERE Customer_ID = ' + str(self.customerID))
            self.customerName = mycursor.fetchall()
            self.customerName1 = self.customerName[0][1] + " " + self.customerName[0][2]
            print(self.customerName1)

            if (self.completed == 0):
                print("Pending")
            else:
                print("Completed")

            print("----------------------------")



            # print(order)
       

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login In")
        self.geometry("300x200")

        Label(self, text="Username").place(x=20, y=10)
        self.userName = ttk.Entry(self)
        self.userName.place(x=20, y=30)

        Label(self, text="Password").place(x=20, y=70)
        self.password = ttk.Entry(self, show="*")
        self.password.place(x=20, y=90)


        self.loginBtn = ttk.Button(self, text='Login')
        self.loginBtn['command'] = self.loginUser
        self.loginBtn.place(x=180, y=60)

        # self.loginBtn = ttk.Button(self, text="Login", command=self.loginUser).place(x=120, y=120)
        self.closeBtn = ttk.Button(self, text="Close", command=self.destroy).place(x=5, y=170)

        # self.encrptBtn = ttk.Button(self, text="encrypt", command=self.giveEncrptedPasswords).place(x=100, y=120)

    def loginUser(self):
        self.Key = b'l2ihTWOCdrskUed1cWfgMGQzwGOSD3EiKZ0IxWQGpzc='
        # print(self.Key)
        self.fernet = Fernet(self.Key)
        # self.encPassword = self.fernet.encrypt((self.password.get()).encode())

        # print(self.encPassword)
        # print(len(self.encPassword))

        # self.decMessage = self.fernet.decrypt(self.encPassword).decode()
        check = False
        mycursor.execute('SELECT * FROM sys.employee')
        employees = mycursor.fetchall()
        for employee in employees:
            self.decMessage = self.fernet.decrypt(employee[8].encode()).decode()
            if ((self.password.get() == self.decMessage) and (self.userName.get() == employee[7])):
                if (employee[6] == "Server"):
                    self.destroy()
                    ServerView(employee)
                elif (employee[6] == "Cook"):
                    print("I am a cook")
                elif (employee[6] == "Manager"):
                    print("I am a manager")
                check = True
                break
        if (not check):
            messagebox.showwarning("showwarning", "Incorrect Login! Please Try Again")

        # print(self.decMessage)
    

if __name__ == "__main__":
    # app = ViewOrders("Something")
    app = LoginView()
    app.mainloop()


