import os
import datetime as time
clear = lambda: os.system('clear' if os.name != 'nt' else 'cls')
import mysql.connector as con
passwd = input("Enter password: ") #insql777
mycon=con.connect(host='localhost',user='root',password=passwd)
cur=mycon.cursor()
cur.execute("create database if not exists store;")
cur.execute("use store;")
cur.execute("create table if not exists inventory(name varchar(100), price varchar(10), qty int, expdate date);")
veg=["Potato","Brinjal","Banana","Tomato","Onion","Apple","Mango","Grapes","Flour","Pear","Guava","Pineapple","Papaya","Pomegranate","Milk","Paneer"]


rn=time.datetime.today()
shortDelta=time.timedelta(days=7)
longDelta=time.timedelta(days=180)  
shortExpiry=rn+shortDelta
longExpiry=rn+longDelta
shortExpiry=shortExpiry.date()
longExpiry=longExpiry.date()
shortExpiry=shortExpiry.strftime('%Y-%m-%d')
longExpiry=longExpiry.strftime('%Y-%m-%d')

def main():
    clear()
    print("***********************")
    print("       StoreSync")
    print("***********************")
    print("What would you like to do?")
    print("Press 1 : Add items to inventory")
    print("Press 2 : View inventory")
    print("Enter (B) to break")
    while True:
        userinput=input("Enter number according to required action: ").lower()
        if userinput=="1":
            additems()
            break
        elif userinput=="2":
            viewinventory()
            break
        elif userinput=="b": 
            break

def additems():
    clear()
    print("**********************")
    print("ADD ITEMS TO INVENTORY")
    print("**********************")
    while True:
        num=input("Enter number of items to be added: ")
        if num.isdigit() and int(num) > 0:
            break
        else:
            print("Please enter a valid positive number")
    num=int(num)
    for i in range(1,num+1):
        while True:
            useritem=input("Enter item name: ")
            cur.execute("select * from inventory")
            data=cur.fetchall()
            l1=[]
            for row in data:
                x=row[0]
                l1.append(x)
                
            if useritem != "" and useritem not in l1:
                break 
            else:
                print("Item already exists")  
                continue
        while True:
            itemprice=input("Price of Item: ")
            if itemprice.isdigit():
                break
        while True:
            itemqty=int(input("Enter qty of item: "))
            if type(itemqty) is int: 
                break
        if useritem in veg:
            insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
            insert_tup=(useritem,itemprice,itemqty,shortExpiry)
            cur.execute(insert,insert_tup)
        else:
            insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
            insert_tup=(useritem,itemprice,itemqty,longex)
            cur.execute(insert,insert_tup)
        mycon.commit()
    if num == 1:
        returntomenu("Item has been successfully added.")
    else:
        returntomenu("Items have been successfully added.")
        
def viewinventory():
    clear()
    print("VIEW INVENTORY")
    print("**************")
    cur.execute("select * from inventory")
    data=cur.fetchall()
    print("ITEMS")
    print("*****")
    for row in data:
        print(f"{row[0]}: {row[1]} (Qty: {row[2]})")
    print()
    print("Options:")
    print("Enter (B) to go back")
    print("Enter 1 to edit item")
    print("Enter 2 to delete item")
    print("Enter 3 to get item details")
    while True:
        userinput=input("Enter number corresponding to required action: ").lower()
        if userinput=="1":
            editinventory()
            break
        elif userinput=="2":
            deleteitem()
            break
        elif userinput=="3": 
            while True: 
                def Details(): 
                    itemname=input("Enter item name to get details: ")
                    cur.execute("select * from inventory")
                    data=cur.fetchall()
                    l2=[]
                    for i in data:
                        l2.append(i[0])
                        if itemname in l2:
                            print()
                            print(" Item name:",i[0],'\n',"Item Price:",i[1],'\n',"Quantity:",i[2],'\n',"Expiry:",i[3])
                            print()
                            break
                    else:
                        print("Item does not exist")
                Details()
                        
                while True: 
                    print("ANSWER IN YES/NO")
                    quest=input("Do you want details of more items? ").lower()
                    if quest=="yes": 
                        Details()
                    elif quest=="no":
                        viewinventory()
                        break       
                    else:
                        pass
                    
        elif userinput=="b" :
            main()
            break
    
def editinventory():
    clear()
    print("EDIT INVENTORY ITEM")
    print("*******************")
    print("Options:")
    print("Enter (B) to return to menu")
    print("Enter 1 to edit Item details")
   
    while True:
        userinput=input("Choose option: ").lower()
        if userinput in ["1","2","3","b"]:
            break
    if userinput=="b":
        main()
    if userinput=="1":
        def Tablechange():
            clear()
            print("Enter (B) to go back to view inventory")
            print("ITEM DETAILS")
            print()
            cur.execute("select * from inventory")
            stuff=cur.fetchall()

            dict1={}
            for i in range(len(stuff)):
                dict1[i+1]=stuff[i]
            print ("{:<8} {:<15} {:<10} {:<10} ".format('Sno.','Iname','Price','Qty'))
            for k, v in dict1.items():
                iname1,price1,qty1,expdate1=v
                print ("{:<8} {:<15} {:<10} {:<10}".format(k,iname1,price1,qty1))
            edit=input("What would you like to edit from the above? ").lower()
            if edit=="iname":
                while True: 
                    itemname=input("Enter the item to change: ")
                    cur.execute("select Iname from inventory")
                    data=cur.fetchall()
                    for i in data: 
                        if i[0]==itemname:
                            itemname2=input("Enter the new name: ")
                            change=("update inventory set Iname=%s where Iname=%s")                    
                            print("Data has been changed! ")
                            change2=(itemname2,itemname)
                            cur.execute(change,change2)
                            mycon.commit()
                            print("ANSWER IN Yes/No")
                            a=input("Would you like to edit any other name? ").lower()
                            if a=="yes":
                                continue
                            else:
                                clear()
                                Tablechange()
                        elif itemname=="b":
                            editinventory()
                
            elif edit=="price": 
                 
                while True: 
                    name_price=input("Which item's price would you like to change? ")
                    cur.execute("select Iname from inventory")
                    data=cur.fetchall()
                    for i in data: 
                        if i[0]==name_price: 
                            itemprice=input("Enter the new price: ")
                            change=("update inventory set Price=%s where Iname=%s")
                            change2=(itemprice,name_price)
                            cur.execute(change,change2)
                            mycon.commit()
                            print("Data has been changed! ")
                            print("ANSWER IN Yes/No")
                            a=input("Would you like to edit any other price? ").lower()
                            if a=="yes":
                                continue
                            else:
                                clear()
                                Tablechange()
                        elif name_price=="b":
                            editinventory()
            elif edit=="qty":
                
                while True: 
                    name_qty=input("Which item's qty would you like to change? ")
                    cur.execute("select Iname from inventory")
                    data=cur.fetchall()
                    for i in data: 
                        if i[0]==name_qty: 
                            itemqty=input("Enter the new Quantity: ")
                            change=("update inventory set qty=%s where Iname=%s")
                            change2=(itemqty,name_qty)
                            cur.execute(change,change2)
                            mycon.commit()
                            print("Data has been changed! ")
                            print("ANSWER IN Yes/No")
                            a=input("Would you like to edit any other price? ").lower()
                            if a=="yes":
                                continue
                            else:
                                clear()
                                Tablechange()
                        elif name_qty=="b":
                            editinventory()
                
            else:
                clear()
                editinventory()
        Tablechange()
    else: 
        print("Error! Field does not exist")               

        
        
def deleteitem():
    clear()
    print("DELETE ITEM FROM INVENTORY")
    print("**************************")
    print("ITEM DETAILS")
    print()
    cur.execute("select * from inventory")
    stuff=cur.fetchall()
    dict1={}
    for i in range(len(stuff)):
        dict1[i+1]=stuff[i]
    print ("{:<8} {:<15} {:<10} {:<10} ".format('Sno.','Iname','Price','Qty'))
    for k, v in dict1.items():
        iname1,price1,qty1,expdate1=v
        print ("{:<8} {:<15} {:<10} {:<10}".format(k,iname1,price1,qty1))
    print()
    cur.execute("select Iname from inventory")
    existing_items=[row[0] for row in cur.fetchall()]
    while True:
        itemtodel=input("Enter name of item to be deleted: ")
        if itemtodel in existing_items:
            break
        else:
            print("Error! Item does not exist")

    while True:
        confrm=input("Are you sure you want to delete this item?: ").lower()
        if confrm in ["yes","no"]:
            break
    if confrm=="yes":
        delstr="delete from inventory where Iname=%s"
        delvalue=(itemtodel,)
        cur.execute(delstr,delvalue)
        mycon.commit()
        returntomenu("Item has been successfully deleted.")
    else:
        main()
    
           

def returntomenu(message):
    while True:
        back=input(f"{message}.Press (M) to return to main menu: ").lower()
        if back=="m":
            main()
            break
main()

cur.close()
