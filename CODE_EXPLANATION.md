# Detailed Line-by-Line Code Explanation

## **Lines 1-3: Import Statements and Clear Screen Function**

```python
import os
```
- Imports the `os` module to interact with the operating system (used for clearing screen)

```python
import datetime as time
```
- Imports Python's `datetime` module and renames it to `time` (shorter alias for convenience)

```python
clear = lambda: os.system('clear' if os.name != 'nt' else 'cls')
```
- Creates a lambda function called `clear` that clears the terminal screen
- Uses `'clear'` command on Unix/macOS (when `os.name != 'nt'`)
- Uses `'cls'` command on Windows (when `os.name == 'nt'`)

---

## **Lines 4-6: Database Connection Setup**

```python
import mysql.connector as con
```
- Imports the MySQL connector library and renames it to `con` for brevity
- This library allows Python to connect to MySQL databases

```python
mycon=con.connect(host='localhost',user='root',password='insql777')
```
- Establishes a connection to MySQL database server
- `host='localhost'`: Connects to MySQL running on the same machine
- `user='root'`: Uses the root user account
- `password='insql777'`: Provides the password for authentication
- Stores the connection object in variable `mycon`

```python
cur=mycon.cursor()
```
- Creates a cursor object from the database connection
- A cursor is needed to execute SQL queries and fetch results
- Stores it in variable `cur`

---

## **Lines 7-9: Database and Table Creation**

```python
cur.execute("create database if not exists GeneralStore;")
```
- Executes SQL command to create a database named "GeneralStore"
- `IF NOT EXISTS` prevents error if database already exists
- This is a DDL (Data Definition Language) command

```python
cur.execute("use GeneralStore;")
```
- Switches to the "GeneralStore" database
- All subsequent operations will be performed on this database

```python
cur.execute("create table if not exists Inventory(Iname varchar(100),Price varchar(10),qty int,expdate date);")
```
- Creates a table named "Inventory" if it doesn't already exist
- Table structure:
  - `Iname varchar(100)`: Item name, up to 100 characters
  - `Price varchar(10)`: Price stored as string, up to 10 characters
  - `qty int`: Quantity as integer
  - `expdate date`: Expiry date in date format

---

## **Lines 10-19: Date Calculations for Expiry**

```python
veg=["Potato","Brinjal","Banana","Tomato","Onion","Apple","Mango","Grapes","Flour","Pear","Guava","Pineapple","Papaya","Pomegranate","Milk","Paneer"]
```
- Defines a list of vegetable/perishable items
- Items in this list will get a shorter expiry date (7 days)
- Other items get a longer expiry date (180 days)

```python
x=time.datetime.today()
```
- Gets the current date and time as a datetime object
- Stores it in variable `x`

```python
deltat=time.timedelta(days=7)
```
- Creates a time delta of 7 days
- Used for perishable items' expiry date

```python
deltat2=time.timedelta(days=180)
```
- Creates a time delta of 180 days
- Used for non-perishable items' expiry date

```python
y=x+deltat
```
- Adds 7 days to current date
- `y` will be used as expiry date for vegetables/perishables

```python
z=x+deltat2
```
- Adds 180 days to current date
- `z` will be used as expiry date for non-perishables

```python
y=y.date()
```
- Converts datetime object `y` to date object (removes time component)

```python
z=z.date()
```
- Converts datetime object `z` to date object (removes time component)

```python
y=y.strftime('%Y-%m-%d')
```
- Formats date `y` as string in 'YYYY-MM-DD' format
- Required for MySQL DATE type insertion

```python
z=z.strftime('%Y-%m-%d')
```
- Formats date `z` as string in 'YYYY-MM-DD' format
- Required for MySQL DATE type insertion

---

## **Lines 20-37: Main Menu Function**

```python
def main():
```
- Defines the main function - entry point of the application

```python
    clear()
```
- Clears the terminal screen for clean display

```python
    print("GENERAL STORE INVENTORY")
    print("***********************")
```
- Prints header/title of the application

```python
    print("What would you like to do?")
    print("Enter 1 to add items to inventory")
    print("Enter 2 to View inventory")
    print("Enter (B) to break")
```
- Displays menu options to the user

```python
    while True:
```
- Creates an infinite loop to keep asking for input until valid option is chosen

```python
        userinput=input("Enter number according to required action: ").lower()
```
- Gets user input and converts to lowercase for case-insensitive comparison

```python
        if userinput=="1":
            additems()
            break
```
- If user enters "1", calls `additems()` function and exits the loop

```python
        elif userinput=="2":
            viewinventory()
            break
```
- If user enters "2", calls `viewinventory()` function and exits the loop

```python
        elif userinput=="b":
            break
```
- If user enters "b", exits the loop (program ends)

---

## **Lines 39-85: Add Items Function**

```python
def additems():
```
- Defines function to add items to inventory

```python
    clear()
    print("ADD ITEMS TO INVENTORY")
    print("**********************")
```
- Clears screen and displays header

```python
    while True:
        num=input("Enter number of items to be added: ")
        if num.isdigit() and int(num) > 0:
            break
        else:
            print("Please enter a valid positive number")
```
- Loops until user enters a valid positive integer
- `isdigit()` checks if input contains only digits
- `int(num) > 0` ensures it's positive

```python
    num=int(num)
```
- Converts validated string input to integer

```python
    for i in range(1,num+1):
```
- Loops from 1 to `num` (inclusive) to process each item

```python
        while True:
            useritem=input("Enter item name: ")
            cur.execute("select * from inventory")
            data=cur.fetchall()
```
- Gets item name from user
- Executes SQL query to fetch all existing items from database
- `fetchall()` retrieves all rows returned by the query

```python
            l1=[]
            for row in data:
                x=row[0]
                l1.append(x)
```
- Creates empty list `l1`
- Loops through each row in database results
- Extracts item name (first column, index 0) from each row
- Appends item name to list `l1`

```python
            if useritem != "" and useritem not in l1:
                break 
            else:
                print("Item already exists")  
                continue
```
- Checks if item name is not empty and not already in database
- If valid, breaks out of validation loop
- If invalid, prints error and continues asking for new name

```python
        while True:
            itemprice=input("Price of Item: ")
            if itemprice.isdigit():
                break
```
- Loops until user enters a valid price (digits only)

```python
        while True:
            itemqty=int(input("Enter qty of item: "))
            if type(itemqty) is int: 
                break
```
- Loops until user enters a valid quantity (integer)
- Note: This validation always passes since `int()` would raise error if invalid

```python
        if useritem in veg:
```
- Checks if the item is in the vegetable/perishable list

```python
            insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
            insert_tup=(useritem,itemprice,itemqty,y)
            cur.execute(insert,insert_tup)
```
- If perishable: Creates SQL INSERT statement with placeholders
- `insert_tup` contains values: item name, price, quantity, and expiry date `y` (7 days)
- Executes the INSERT query with parameterized values (prevents SQL injection)

```python
        else:
            insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
            insert_tup=(useritem,itemprice,itemqty,z)
            cur.execute(insert,insert_tup)
```
- If non-perishable: Similar INSERT but uses expiry date `z` (180 days)

```python
        mycon.commit()
```
- Commits the transaction to save changes to database
- Required after INSERT/UPDATE/DELETE operations

```python
    if num == 1:
        returntomenu("Item has been successfully added.")
    else:
        returntomenu("Items have been successfully added.")
```
- After all items added, shows success message
- Uses singular "Item" for 1 item, plural "Items" for multiple

---

## **Lines 87-142: View Inventory Function**

```python
def viewinventory():
```
- Defines function to view and manage inventory

```python
    clear()
    print("VIEW INVENTORY")
    print("**************")
```
- Clears screen and displays header

```python
    cur.execute("select * from inventory")
    data=cur.fetchall()
```
- Executes SQL SELECT query to get all items
- Fetches all rows into `data`

```python
    print("ITEMS")
    print("*****")
    for row in data:
        print(f"{row[0]}: {row[1]} (Qty: {row[2]})")
```
- Prints header, then loops through each row
- Displays: Item Name (row[0]): Price (row[1]) (Qty: row[2])
- Uses f-string for formatted output

```python
    print()
    print("Options:")
    print("Enter (B) to go back")
    print("Enter 1 to edit item")
    print("Enter 2 to delete item")
    print("Enter 3 to get item details")
```
- Displays submenu options

```python
    while True:
        userinput=input("Enter number corresponding to required action: ").lower()
        if userinput=="1":
            editinventory()
            break
        elif userinput=="2":
            deleteitem()
            break
```
- Gets user choice and calls appropriate function

```python
        elif userinput=="3":
            while True: 
                def Details():
```
- Nested function definition for getting item details
- Note: Function defined inside while loop (not ideal practice)

```python
                    itemname=input("Enter item name to get details: ")
                    cur.execute("select * from inventory")
                    data=cur.fetchall()
                    l2=[]
                    for i in data:
                        l2.append(i[0])
                        if itemname in l2:
```
- Gets item name from user
- Fetches all items from database
- Creates list of item names
- Checks if entered name exists in list

```python
                            print()
                            print(" Item name:",i[0],'\n',"Item Price:",i[1],'\n',"Quantity:",i[2],'\n',"Expiry:",i[3])
                            print()
                            break
```
- If found, prints formatted details with newlines (`\n`)
- Displays name, price, quantity, expiry date
- Breaks out of loop

```python
                    else:
                        print("Item does not exist")
                Details()
```
- If item not found, prints error message
- Calls the nested `Details()` function

```python
                while True: 
                    print("ANSWER IN YES/NO")
                    quest=input("Do you want details of more items? ").lower()
                    if quest=="yes": 
                        Details()
                    elif quest=="no":
                        viewinventory()
                        break
```
- Asks if user wants to see more item details
- If yes, calls `Details()` again
- If no, returns to view inventory menu

```python
        elif userinput=="b" :
            main()
            break
```
- Returns to main menu if user enters "b"

---

## **Lines 144-250: Edit Inventory Function**

```python
def editinventory():
```
- Defines function to edit inventory items

```python
    clear()
    print("EDIT INVENTORY ITEM")
    print("*******************")
    print("Options:")
    print("Enter (B) to return to menu")
    print("Enter 1 to edit Item details")
```
- Clears screen and shows edit menu

```python
    while True:
        userinput=input("Choose option: ").lower()
        if userinput in ["1","2","3","b"]:
            break
```
- Validates user input against allowed options

```python
    if userinput=="b":
        main()
```
- Returns to main menu if "b" entered

```python
    if userinput=="1":
        def Tablechange():
```
- Defines nested function to handle table editing
- Note: Function defined inside if statement

```python
            clear()
            print("Enter (B) to go back to view inventory")
            print("ITEM DETAILS")
            print()
            cur.execute("select * from inventory")
            stuff=cur.fetchall()
```
- Clears screen, fetches all items from database

```python
            dict1={}
            for i in range(len(stuff)):
                dict1[i+1]=stuff[i]
```
- Creates dictionary where keys are serial numbers (1, 2, 3...)
- Values are the row tuples from database

```python
            print ("{:<8} {:<15} {:<10} {:<10} ".format('Sno.','Iname','Price','Qty'))
```
- Prints table header with formatted columns
- `{:<8}` means left-aligned in 8 character width

```python
            for k, v in dict1.items():
                iname1,price1,qty1,expdate1=v
                print ("{:<8} {:<15} {:<10} {:<10}".format(k,iname1,price1,qty1))
```
- Loops through dictionary items
- Unpacks row tuple into individual variables
- Prints formatted table row

```python
            edit=input("What would you like to edit from the above? ").lower()
```
- Asks what field user wants to edit (iname, price, or qty)

```python
            if edit=="iname":
                while True: 
                    itemname=input("Enter the item to change: ")
                    cur.execute("select Iname from inventory")
                    data=cur.fetchall()
                    for i in data: 
                        if i[0]==itemname:
```
- If editing item name, gets current item name
- Fetches all item names from database
- Checks if entered name exists

```python
                            itemname2=input("Enter the new name: ")
                            change=("update inventory set Iname=%s where Iname=%s")
                            print("Data has been changed! ")
                            change2=(itemname2,itemname)
                            cur.execute(change,change2)
                            mycon.commit()
```
- Gets new item name
- Creates SQL UPDATE statement with placeholders
- Executes update query (replaces old name with new name)
- Commits changes to database

```python
                            print("ANSWER IN Yes/No")
                            a=input("Would you like to edit any other name? ").lower()
                            if a=="yes":
                                continue
                            else:
                                clear()
                                Tablechange()
```
- Asks if user wants to edit more names
- If yes, continues loop
- If no, clears screen and shows table again

```python
                        elif itemname=="b":
                            editinventory()
```
- If user enters "b", returns to edit menu

```python
            elif edit=="price":
```
- Similar structure for editing price
- Creates UPDATE query for Price column

```python
            elif edit=="qty":
```
- Similar structure for editing quantity
- Creates UPDATE query for qty column

```python
            else:
                clear()
                editinventory()
```
- If invalid field entered, returns to edit menu

```python
        Tablechange()
```
- Calls the nested function to start editing

```python
    else: 
        print("Error! Field does not exist")
```
- Error message for invalid option

---

## **Lines 254-290: Delete Item Function**

```python
def deleteitem():
```
- Defines function to delete items from inventory

```python
    clear()
    print("DELETE ITEM FROM INVENTORY")
    print("**************************")
    print("ITEM DETAILS")
    print()
```
- Clears screen and shows header

```python
    cur.execute("select * from inventory")
    stuff=cur.fetchall()
    dict1={}
    for i in range(len(stuff)):
        dict1[i+1]=stuff[i]
```
- Fetches all items and creates dictionary with serial numbers

```python
    print ("{:<8} {:<15} {:<10} {:<10} ".format('Sno.','Iname','Price','Qty'))
    for k, v in dict1.items():
        iname1,price1,qty1,expdate1=v
        print ("{:<8} {:<15} {:<10} {:<10}".format(k,iname1,price1,qty1))
```
- Displays formatted table of all items

```python
    cur.execute("select Iname from inventory")
    existing_items=[row[0] for row in cur.fetchall()]
```
- Fetches all item names and creates list using list comprehension
- Used for validation

```python
    while True:
        itemtodel=input("Enter name of item to be deleted: ")
        if itemtodel in existing_items:
            break
        else:
            print("Error! Item does not exist")
```
- Validates that entered item name exists in database

```python
    while True:
        confrm=input("Are you sure you want to delete this item?: ").lower()
        if confrm in ["yes","no"]:
            break
```
- Asks for confirmation before deletion

```python
    if confrm=="yes":
        delstr="delete from inventory where Iname=%s"
        delvalue=(itemtodel,)
        cur.execute(delstr,delvalue)
        mycon.commit()
        returntomenu("Item has been successfully deleted.")
```
- If confirmed, creates DELETE SQL statement
- Note: `delvalue=(itemtodel,)` - comma creates tuple (required for single parameter)
- Executes deletion and commits changes

```python
    else:
        main()
```
- If not confirmed, returns to main menu

---

## **Lines 294-299: Return to Menu Function**

```python
def returntomenu(message):
```
- Helper function to return to main menu after operations

```python
    while True:
        back=input(f"{message}.Press (M) to return to main menu: ").lower()
        if back=="m":
            main()
            break
```
- Displays success message
- Waits for user to press "M" to return to main menu
- Uses f-string for message formatting

---

## **Lines 300-302: Program Entry Point and Cleanup**

```python
main()
```
- Calls main function to start the program
- This is executed when script is run

```python
cur.close()
```
- Closes the database cursor (cleanup)
- Note: This line may not execute if program doesn't exit normally
- Should ideally be in a try-finally block

---

## **Summary**

This is an inventory management system that:
1. Connects to MySQL database
2. Creates database and table if needed
3. Allows adding items with automatic expiry date assignment
4. Allows viewing, editing, and deleting items
5. Uses database as the only storage (no file operations)
6. Provides a command-line menu interface

