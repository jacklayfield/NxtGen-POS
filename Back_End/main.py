import mysql.connector

mydb = mysql.connector.connect(
    host='Localhost',
    user='root',
    password='Fode1234',
    port='3306',
    database='sys'
)

mycursor = mydb.cursor()

mycursor.execute('SELECT * FROM sys.customer')

customers = mycursor.fetchall()

for customer in customers:
    # if customer[7] == 'Manager':
    print(customer)

# if __name__ == '__main__':
