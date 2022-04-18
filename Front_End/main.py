from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from venv import create
import mysql.connector

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
        args = (newID, self.FName.get(), self.LName.get(), self.Email.get(), self.Notes.get())
        query = "INSERT INTO customer(Customer_ID, FName, LName, Email, General_Notes) VALUES" + str(args)
        mycursor.execute(query)
        mydb.commit()
        # print(query)c
        self.destroy()
        serverview = ServerView()

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

    def createOrder(self):
        print("New Order")

    def viewOrder(self):
        print("View Order")

    def createNewCustomer(self):
        self.destroy()
        cust = NewCustomer()
        cust.mainloop()
        print("Create New Customer")


if __name__ == "__main__":
    app = ServerView()
    app.mainloop()


