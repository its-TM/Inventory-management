import os
import datetime as time
clear= lambda: os.system("cls")
import mysql.connector as con
mycon=con.connect(host='localhost',user='root',password='Tanmay10')
cur=mycon.cursor()
cur.execute("create database if not exists GeneralStore;")
cur.execute("use GeneralStore;")
cur.execute("create table if not exists Inventory(Iname varchar(100),Price varchar(10),qty int,expdate date);")
veg=["Potato","Brinjal","Banana","Tomato","Onion","Apple","Mango","Grapes","Flour","Pear","Guava","Pineapple","Papaya","Pomegranate","Milk","Paneer"]
x=time.datetime.today()
deltat=time.timedelta(days=7)
deltat2=time.timedelta(days=180)  
y=x+deltat
z=x+deltat2
y=y.date()
z=z.date()
y=y.strftime('%Y-%m-%d')
z=z.strftime('%Y-%m-%d')
def main():
    clear()
    print("GENERAL STORE INVENTORY")
    print("***********************")
    print("What would you like to do?")
    print("Enter 1 to add items to inventory")
    print("Enter 2 to View inventory")
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
    print("ADD ITEMS TO INVENTORY")
    print("**********************")
    print("Options:")
    print("Enter 1 to add more than 1 item")
    print("Enter 2 to add 1 item")
    while True:
        userinput=input("Enter number corresponding to required action: ")
        if userinput in ["1","2"]:
            break
    if userinput=="1":
        while True:
            num=input("Enter number of items to be added: ")
            if num.isdigit():
                break
        num=int(num)
        items={}
        for i in range(1,num+1):
            while True:
                useritem=input("Enter item name: ")
                cur.execute("select * from inventory")
                data=cur.fetchall()
                l1=[]
                for i in data:
                    x=i[0]
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
            items.update({useritem:int(itemprice)})
            while True:
                itemqty=int(input("Enter qty of item: "))
                if type(itemqty) is int: 
                    break
            items.update({useritem:int(itemprice)})
            if useritem in veg:
                insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
                insert_tup=(useritem,itemprice,itemqty,y)
                cur.execute(insert,insert_tup)
            else:
                insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
                insert_tup=(useritem,itemprice,itemqty,z)
                cur.execute(insert,insert_tup)
            mycon.commit()
        additemstofile(items, clear=False)
        returntomenu("Items have been successfully added.")
    elif userinput=="2":
        items={}
        
        while True:
            useritem=input("Enter item name: ")
            cur.execute("select * from inventory")
            data=cur.fetchall()
            l1=[]
            for i in data:
                x=i[0]
                l1.append(x)
            if useritem != "" and useritem not in l1:
                break
            else:
                print('Item already exists')
                continue
        while True:
            itemprice=input("Price of item: ")
            if itemprice.isdigit():
                break
        while True:
                itemqty=int(input("Enter qty of item: "))
                if type(itemqty) is int: 
                    break
        items.update({useritem:int(itemprice)})
        if useritem in veg:
            insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
            insert_tup=(useritem,itemprice,itemqty,y)
            cur.execute(insert,insert_tup)
        else:
            insert= "INSERT into Inventory (Iname,Price,qty,expdate) values(%s,%s,%s,%s);"
            insert_tup=(useritem,itemprice,itemqty,z)
            cur.execute(insert,insert_tup)

        mycon.commit()
        additemstofile({useritem: int(itemprice)}, clear=False)
        returntomenu("Item has been successfully added.")
        
def viewinventory():
    clear()
    print("VIEW INVENTORY")
    print("**************")
    invitems=getitems()
    print("ITEMS")
    print("*****")
    for i in invitems:
        print(f"{i}:{invitems[i]}")
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
    invitems=getitems()
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
                            templist={}
                            for m,n in invitems.items(): 
                                if m == itemname: 
                                    templist[itemname2]= n 
                                else: 
                                    templist[m]= n
                            additemstofile(templist,clear=True)
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
                            invitems.update({name_price:itemprice})
                            additemstofile(invitems,clear=True)
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
    invitems=getitems()
    while True:
        itemtodel=input("Enter name of item to be deleted: ")
        if itemtodel in invitems:
            break
        else:
            print("Error! Item does not exist")

    while True:
        confrm=input("Are you sure you want to delete this item?: ").lower()
        if confrm in ["yes","no"]:
            break
    if confrm=="yes":
        del invitems[itemtodel]
        delstr="delete from inventory where Iname=%s"
        delvalue=(itemtodel,)
        cur.execute(delstr,delvalue)
        mycon.commit()
        additemstofile(invitems,clear=True)
        returntomenu("Item has been successfully deleted.")
    else:
        main()
    
def additemstofile(items: dict,clear:bool):
    if clear:
        f=open("items.txt","w")
        f.close()
        with open("items.txt","a") as file:
            for i in items:
                file.write(f"{i}:{items[i]}")
                file.write("\n")
        return
    invitems=getitems()
    for i in invitems:
        if i in items:
            items[i]+=invitems[i]
 
    with open("items.txt","a") as file:
        for i in items:
            file.write(f"{i}:{items[i]}")
            file.write("\n")
    
def getitems():
    invitems={}
    with open("items.txt","r") as file:
        for l in file:
            l=l.replace("\n","").split(":")
            itemname,itemprice=l[0],l[1].strip()
            invitems.update({itemname:int(itemprice)})
    return invitems
           

def returntomenu(message):
    while True:
        back=input(f"{message}.Press (M) to return to main menu: ").lower()
        if back=="m":
            main()
            break
main()

cur.close()
