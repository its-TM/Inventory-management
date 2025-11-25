import os
import datetime as time
clear = lambda: os.system('clear' if os.name != 'nt' else 'cls')
import mysql.connector as con
passwd = input("Enter password: ") #insql777
mycon=con.connect(host='localhost',user='root',password=passwd)
cur=mycon.cursor()
cur.execute("create database if not exists store;")
cur.execute("use store;")

def execute_sql_and_commit(cur, conn, sql, log_message=""):
    """Executes a single SQL statement and commits the transaction."""
    if not sql.strip():
        return
    
    try:
        cur.execute(sql)
        conn.commit()
        if log_message:
            print(f"SUCCESS: {log_message}")
    except Exception as e:
        # Ignore common non-critical errors for DROP and CREATE IF NOT EXISTS
        error_msg = str(e).lower()
        if "does not exist" in error_msg or "already exists" in error_msg:
             return # Just suppress and continue
        # Raise other critical errors
        print(f"FATAL ERROR executing SQL: {e}\nSQL: {sql.strip()[:100]}...")
        conn.rollback()
        raise e

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

def fetch_inventory():
    # IFNULL keeps the listing readable even when category or supplier data is missing.
    cur.execute("""
        select i.name,
               ifnull(i.category,'Uncategorized') as category,
               i.price,
               i.qty,
               i.expdate,
               i.supplier_id,
               ifnull(s.supplier_name,'Unassigned') as supplier_name
        from inventory i
        left join suppliers s on i.supplier_id=s.supplier_id
    """)
    return cur.fetchall()

def fetch_item_names():
    cur.execute("select name from inventory")
    return [row[0] for row in cur.fetchall()]

def prompt_yes_no(message):
    while True:
        answer=input(message).strip().lower()
        if answer in ["yes","no"]:
            return answer=="yes"
        print("Please answer with yes or no.")

def display_inventory_list(items):
    if not items:
        print("Inventory is currently empty.")
        return
    print("Item List:")
    counter=1
    for row in items:
        name,category,price,qty,expdate,_,supplier_name=row
        print(f"{counter}. {name} [{category}] | Price: ₹{price} | Qty: {qty} | Supplier: {supplier_name} | Exp: {expdate}")
        counter+=1

def fetch_suppliers():
    cur.execute("select supplier_id, supplier_name, contact_info, email from suppliers order by supplier_name")
    return cur.fetchall()

def create_supplier_flow():
    print("Add a new supplier:")
    supplier_name=input("Supplier name: ").strip()
    contact=input("Contact info: ").strip()
    email=input("Email: ").strip()
    cur.execute("insert into suppliers(supplier_name, contact_info, email) values(%s,%s,%s)",(supplier_name,contact,email))
    mycon.commit()
    return cur.lastrowid

def prompt_supplier_selection():
    while True:
        suppliers=fetch_suppliers()
        if suppliers:
            print("Existing suppliers:")
            for sid,name,contact,email in suppliers:
                print(f"{sid}: {name} ({contact})")
        else:
            print("No suppliers found.")
        choice=input("Enter supplier ID, or type 'new' to add one: ").strip().lower()
        if choice=="new":
            return create_supplier_flow()
        if choice.isdigit():
            sid=int(choice)
            if any(sid==row[0] for row in suppliers):
                return sid
        print("Invalid selection. Please try again.")

def prompt_category():
    while True:
        category=input("Enter category: ").strip()
        if category:
            return category
        print("Category cannot be empty.")

def show_item_details_flow():
    while True:
        itemname=input("Enter item name to get details: ").strip()
        if not itemname:
            print("Please enter a valid item name.")
            continue
        cur.execute("""
            select i.name,
                   ifnull(i.category,'Uncategorized'),
                   i.price,
                   i.qty,
                   i.expdate,
                   ifnull(s.supplier_name,'Unassigned'),
                   s.contact_info
            from inventory i
            left join suppliers s on i.supplier_id=s.supplier_id
            where i.name=%s
        """,(itemname,))
        data=cur.fetchone()
        if data:
            name,category,price,qty,expdate,supplier_name,contact=data
            print()
            print(" Item name:",name)
            print(" Category:",category)
            print(" Item Price:",price)
            print(" Quantity:",qty)
            print(" Expiry:",expdate)
            print(" Supplier:",supplier_name)
            print(" Supplier Contact:",contact or "N/A")
            print()
        else:
            print("Item does not exist.")
        if not prompt_yes_no("Do you want details of more items? (yes/no): "):
            return

TABLE_SQLS = [
    """
    create table if not exists suppliers(
        supplier_id int auto_increment primary key,
        supplier_name varchar(100),
        contact_info varchar(100),
        email varchar(100)
    )
    """,
    """
    create table if not exists inventory(
        name varchar(100) primary key,
        category varchar(50),
        price varchar(10),
        qty int,
        expdate date,
        supplier_id int,
        foreign key (supplier_id) references suppliers(supplier_id)
    )
    """,
    """
    create table if not exists inventory_thresholds(
        item_name varchar(100) primary key,
        reorder_level int default 5,
        foreign key (item_name) references inventory(name) on delete cascade
    )
    """,
    """
    create table if not exists inventory_notifications(
        notification_id int auto_increment primary key,
        item_name varchar(100),
        qty_snapshot int,
        message varchar(255),
        created_at datetime default current_timestamp
    )
    """,
    """
    create table if not exists price_history(
        history_id int auto_increment primary key,
        item_name varchar(100),
        old_price varchar(10),
        new_price varchar(10),
        changed_at datetime default current_timestamp
    )
    """,
    """
    create table if not exists daily_expiry_summary(
        summary_id int auto_increment primary key,
        summary_date date,
        category varchar(50),
        items_expiring int,
        unique key uniq_summary(summary_date, category)
    )
    """,
    """
    create table if not exists supplier_contact_audit(
        audit_id int auto_increment primary key,
        supplier_id int,
        old_contact varchar(100),
        new_contact varchar(100),
        changed_at datetime default current_timestamp
    )
    """,
    """
    create table if not exists sales_orders(
        order_id int auto_increment primary key,
        item_name varchar(100),
        reserved_qty int,
        status varchar(20) default 'open'
    )
    """,
    """
    create table if not exists sales_lines(
        line_id int auto_increment primary key,
        item_name varchar(100),
        category varchar(50),
        qty int,
        sold_at datetime default current_timestamp
    )
    """,
    """
    create table if not exists category_sales_stats(
        category varchar(50) primary key,
        total_qty int default 0,
        inventory_value decimal(12,2) default 0,
        last_updated datetime
    )
    """,
    """
    create table if not exists receipts(
        receipt_id int auto_increment primary key,
        supplier_id int,
        delivered_qty int,
        delivered_on date,
        on_time int default 1
    )
    """,
    """
    create table if not exists supplier_scorecard(
        supplier_id int primary key,
        shipments_recorded int default 0,
        on_time_count int default 0,
        last_updated datetime
    )
    """,
    """
    create table if not exists restock_plan(
        plan_id int auto_increment primary key,
        item_name varchar(100),
        planned_date date,
        qty int
    )
    """,
    """
    create table if not exists restock_queue(
        queue_id int auto_increment primary key,
        item_name varchar(100),
        planned_date date,
        qty int
    )
    """,
]

FUNCTION_SQLS = [
    "drop function if exists days_to_expiry",
    """
    create function days_to_expiry(p_item_name varchar(100))
    returns int
    deterministic
    begin
        declare done int default 0;
        declare v_exp date;
        declare cur_exp cursor for
            select expdate from inventory where name=p_item_name order by expdate asc;
        declare continue handler for not found set done=1;
        open cur_exp;
        fetch cur_exp into v_exp;
        if done=1 then
            close cur_exp;
            return null;
        end if;
        close cur_exp;
        return datediff(v_exp, current_date());
    end
    """, 

    "drop function if exists available_qty",
    """
    create function available_qty(p_item_name varchar(100))
    returns int
    deterministic
    begin
        declare done int default 0;
        declare v_reserved int;
        declare v_remaining int default 0;
        declare cur_res cursor for
            select reserved_qty from sales_orders where item_name=p_item_name and status='open';
        declare continue handler for not found set done=1;
        select ifnull(qty,0) into v_remaining from inventory where name=p_item_name limit 1;
        open cur_res;
        read_res: loop
            fetch cur_res into v_reserved;
            if done=1 then
                leave read_res;
            end if;
            set v_remaining = v_remaining - ifnull(v_reserved,0);
        end loop;
        close cur_res;
        return v_remaining;
    end
    """,

    "drop function if exists category_value",
    """
    create function category_value(p_category varchar(50))
    returns decimal(12,2)
    deterministic
    begin
        declare done int default 0;
        declare v_qty int;
        declare v_price decimal(10,2);
        declare v_total decimal(12,2) default 0;
        declare cur_cat cursor for
            select qty, cast(price as decimal(10,2)) from inventory where category=p_category;
        declare continue handler for not found set done=1;
        open cur_cat;
        loop_cat: loop
            fetch cur_cat into v_qty, v_price;
            if done=1 then
                leave loop_cat;
            end if;
            set v_total = v_total + (ifnull(v_qty,0) * ifnull(v_price,0));
        end loop;
        close cur_cat;
        return v_total;
    end
    """,

    "drop function if exists next_restock_date",
    """
    create function next_restock_date(p_item_name varchar(100))
    returns date
    deterministic
    begin
        declare done int default 0;
        declare v_date date;
        declare cur_next cursor for
            select planned_date from restock_queue where item_name=p_item_name order by planned_date asc;
        declare continue handler for not found set done=1;
        open cur_next;
        fetch cur_next into v_date;
        if done=1 then
            close cur_next;
            return null;
        end if;
        close cur_next;
        return v_date;
    end
    """,
]


PROCEDURE_SQLS = [
    "drop procedure if exists restock_item",
    """
    create procedure restock_item(in item_name varchar(100), in qty_to_add int)
    begin
        update inventory set qty = qty + qty_to_add where name = item_name;
    end
    """,

    "drop procedure if exists restock_by_category",
    """
    create procedure restock_by_category(in p_category varchar(50))
    begin
        declare done int default 0;
        declare v_item varchar(100);
        declare v_needed int;
        declare cur_items cursor for
            select i.name, (it.reorder_level - i.qty)
            from inventory i
            join inventory_thresholds it on it.item_name=i.name
            where i.category=p_category and i.qty < it.reorder_level;
        declare continue handler for not found set done=1;
        open cur_items;
        loop_items: loop
            fetch cur_items into v_item, v_needed;
            if done=1 then
                leave loop_items;
            end if;
            if v_needed > 0 then
                insert into restock_queue(item_name, planned_date, qty)
                values(
                    v_item,
                    coalesce(next_restock_date(v_item), date_add(current_date(), interval 2 day)),
                    v_needed
                );
            end if;
        end loop;
        close cur_items;
    end
    """,

    "drop procedure if exists close_day_inventory",
    """
    create procedure close_day_inventory()
    begin
        declare done int default 0;
        declare v_name varchar(100);
        declare v_category varchar(50);
        declare v_days int;
        declare cur_inv cursor for
            select name, ifnull(category,'Uncategorized') from inventory;
        declare continue handler for not found set done=1;
        open cur_inv;
        loop_inv: loop
            fetch cur_inv into v_name, v_category;
            if done=1 then
                leave loop_inv;
            end if;
            set v_days = days_to_expiry(v_name);
            if v_days is not null and v_days <= 14 then
                insert into daily_expiry_summary(summary_date, category, items_expiring)
                values (current_date(), v_category, 1)
                on duplicate key update items_expiring = items_expiring + 1;
            end if;
        end loop;
        close cur_inv;
    end
    """,

    "drop procedure if exists supplier_bulk_update",
    """
    create procedure supplier_bulk_update(in p_old_supplier int, in p_new_supplier int)
    begin
        declare done int default 0;
        declare v_item varchar(100);
        declare cur_items cursor for
            select name from inventory where supplier_id=p_old_supplier;
        declare continue handler for not found set done=1;
        open cur_items;
        supplier_loop: loop
            fetch cur_items into v_item;
            if done=1 then
                leave supplier_loop;
            end if;
            update inventory set supplier_id=p_new_supplier where name=v_item;
        end loop;
        close cur_items;
    end
    """,

    "drop procedure if exists inventory_item_clone",
    """
    create procedure inventory_item_clone(in p_source varchar(100), in p_target varchar(100))
    begin
        declare done int default 0;
        declare v_category varchar(50);
        declare v_price varchar(10);
        declare v_qty int;
        declare v_exp date;
        declare v_supplier int;
        declare cur_source cursor for
            select category, price, qty, expdate, supplier_id from inventory where name=p_source;
        declare continue handler for not found set done=1;
        open cur_source;
        clone_loop: loop
            fetch cur_source into v_category, v_price, v_qty, v_exp, v_supplier;
            if done=1 then
                leave clone_loop;
            end if;
            insert into inventory(name, category, price, qty, expdate, supplier_id)
            values(p_target, v_category, v_price, v_qty, v_exp, v_supplier)
            on duplicate key update
                category=values(category),
                price=values(price),
                qty=values(qty),
                expdate=values(expdate),
                supplier_id=values(supplier_id);
            insert into inventory_thresholds(item_name, reorder_level)
            values(p_target,5)
            on duplicate key update reorder_level=values(reorder_level);
        end loop;
        close cur_source;
    end
    """,

    "drop procedure if exists refresh_low_stock_notifications",
    """
    create procedure refresh_low_stock_notifications()
    begin
        declare done int default 0;
        declare v_name varchar(100);
        declare v_qty int;
        declare v_level int;
        declare cur_low cursor for
            select i.name, i.qty, it.reorder_level
            from inventory i
            join inventory_thresholds it on it.item_name=i.name
            where i.qty < it.reorder_level;
        declare continue handler for not found set done=1;
        delete from inventory_notifications where date(created_at)=current_date();
        open cur_low;
        low_loop: loop
            fetch cur_low into v_name, v_qty, v_level;
            if done=1 then
                leave low_loop;
            end if;
            insert into inventory_notifications(item_name, qty_snapshot, message)
            values(v_name, v_qty, concat('Qty below level: ', v_level));
        end loop;
        close cur_low;
    end
    """,

    "drop procedure if exists update_category_sales",
    """
    create procedure update_category_sales()
    begin
        declare done int default 0;
        declare v_category varchar(50);
        declare v_qty int;
        declare cur_sales cursor for
            select category, sum(qty) from sales_lines group by category;
        declare continue handler for not found set done=1;
        open cur_sales;
        sales_loop: loop
            fetch cur_sales into v_category, v_qty;
            if done=1 then
                leave sales_loop;
            end if;
            insert into category_sales_stats(category, total_qty, inventory_value, last_updated)
            values(v_category, ifnull(v_qty,0), category_value(v_category), now())
            on duplicate key update
                total_qty=values(total_qty),
                inventory_value=values(inventory_value),
                last_updated=values(last_updated);
        end loop;
        close cur_sales;
    end
    """,

    "drop procedure if exists update_supplier_scorecard",
    """
    create procedure update_supplier_scorecard(in p_supplier_id int)
    begin
        declare done int default 0;
        declare v_on_time int;
        declare v_total int default 0;
        declare v_on_time_total int default 0;
        declare cur_ship cursor for
            select on_time from receipts where supplier_id=p_supplier_id;
        declare continue handler for not found set done=1;
        open cur_ship;
        ship_loop: loop
            fetch cur_ship into v_on_time;
            if done=1 then
                leave ship_loop;
            end if;
            set v_total = v_total + 1;
            if ifnull(v_on_time,0)=1 then
                set v_on_time_total = v_on_time_total + 1;
            end if;
        end loop;
        close cur_ship;
        insert into supplier_scorecard(supplier_id, shipments_recorded, on_time_count, last_updated)
        values(p_supplier_id, v_total, v_on_time_total, now())
        on duplicate key update
            shipments_recorded=values(shipments_recorded),
            on_time_count=values(on_time_count),
            last_updated=values(last_updated);
    end
    """,

    "drop procedure if exists sync_restock_queue",
    """
    create procedure sync_restock_queue()
    begin
        declare done int default 0;
        declare v_item varchar(100);
        declare v_date date;
        declare v_qty int;
        declare cur_plan cursor for
            select item_name, planned_date, qty from restock_plan;
        declare continue handler for not found set done=1;
        delete from restock_queue;
        open cur_plan;
        plan_loop: loop
            fetch cur_plan into v_item, v_date, v_qty;
            if done=1 then
                leave plan_loop;
            end if;
            insert into restock_queue(item_name, planned_date, qty)
            values(v_item, v_date, v_qty);
        end loop;
        close cur_plan;
    end
    """,
]

TRIGGER_SQLS = [
    "drop trigger if exists low_stock_cursor",
    """
    create trigger low_stock_cursor after update on inventory
    for each row
    begin
        call refresh_low_stock_notifications();
    end
    """,

    "drop trigger if exists price_change_audit",
    """
    create trigger price_change_audit before update on inventory
    for each row
    begin
        if new.price <> old.price then
            insert into price_history(item_name, old_price, new_price)
            values(old.name, old.price, new.price);
        end if;
    end
    """,

    "drop trigger if exists expiry_bucket_refresh",
    """
    create trigger expiry_bucket_refresh after insert on inventory
    for each row
    begin
        call close_day_inventory();
    end
    """,

    "drop trigger if exists supplier_contact_change",
    """
    create trigger supplier_contact_change after update on suppliers
    for each row
    begin
        if new.contact_info <> old.contact_info then
            insert into supplier_contact_audit(supplier_id, old_contact, new_contact)
            values(old.supplier_id, old.contact_info, new.contact_info);
        end if;
    end
    """,

    "drop trigger if exists reserved_qty_guard",
    """
    create trigger reserved_qty_guard before insert on sales_orders
    for each row
    begin
        if new.reserved_qty > available_qty(new.item_name) then
            signal sqlstate '45000' set message_text='Reserved qty exceeds availability';
        end if;
    end
    """,

    "drop trigger if exists category_sales_rollup",
    """
    create trigger category_sales_rollup after insert on sales_lines
    for each row
    begin
        call update_category_sales();
    end
    """,

    "drop trigger if exists supplier_scorecard_update",
    """
    create trigger supplier_scorecard_update after insert on receipts
    for each row
    begin
        call update_supplier_scorecard(new.supplier_id);
    end
    """,

    "drop trigger if exists restock_plan_sync",
    """
    create trigger restock_plan_sync after update on restock_plan
    for each row
    begin
        call sync_restock_queue();
    end
    """,
]

def setup_sql_assets():
    execute_sql_and_commit(cur, mycon, "SET GLOBAL log_bin_trust_function_creators = 1", "Set log_bin_trust_function_creators")

    print("\n--- Installing Tables ---")
    for i, sql in enumerate(TABLE_SQLS):
        execute_sql_and_commit(cur, mycon, sql, f"Table {i+1}/{len(TABLE_SQLS)}")

    print("\n--- Installing Functions ---")
    for i, sql in enumerate(FUNCTION_SQLS):
        execute_sql_and_commit(cur, mycon, sql, f"Function {i+1}/{len(FUNCTION_SQLS)}")

    print("\n--- Installing Procedures ---")
    for i, sql in enumerate(PROCEDURE_SQLS):
        execute_sql_and_commit(cur, mycon, sql, f"Procedure {i+1}/{len(PROCEDURE_SQLS)}")

    print("\n--- Installing Triggers ---")
    for i, sql in enumerate(TRIGGER_SQLS):
        execute_sql_and_commit(cur, mycon, sql, f"Trigger {i+1}/{len(TRIGGER_SQLS)}")

    print("\n--- SQL Assets Setup Complete ---")
    mycon.commit()

def restock_via_procedure():
    clear()
    print("**************************")
    print("RESTOCK USING STORED PROC")
    print("**************************")
    existing=set(fetch_item_names())
    if not existing:
        input("Inventory is empty. Press Enter to return...")
        return
    while True:
        itemname=input("Enter item to restock (or B to go back): ").strip()
        if itemname.lower()=="b":
            return
        if itemname not in existing:
            print("Item does not exist.")
            continue
        break
    while True:
        qty=input("Enter quantity to add: ").strip()
        if qty.isdigit() and int(qty)>0:
            qty=int(qty)
            break
        print("Please enter a positive number.")
    try:
        mycon.rollback()
        mycon.start_transaction()
        cur.callproc("restock_item",(itemname,qty))
        mycon.commit()
        print("Restock successful via stored procedure.")
    except Exception as exc:
        mycon.rollback()
        print(f"Restock failed: {exc}")
    input("Press Enter to continue...")

def transaction_batch_mode():
    clear()
    print("******************************")
    print("TRANSACTION BATCH MANAGEMENT")
    print("******************************")
    print("Use this mode to apply multiple qty adjustments atomically.")
    existing=set(fetch_item_names())
    if not existing:
        input("Inventory is empty. Press Enter to return...")
        return
    mycon.rollback()
    mycon.start_transaction()
    try:
        while True:
            print("\nOptions: increase, decrease, commit, rollback")
            action=input("Choose action: ").strip().lower()
            if action.lower()=="b":
                return
            if action in ["commit","c"]:
                mycon.commit()
                print("Transaction committed.")
                input("Press Enter to continue...")
                return
            if action in ["rollback","r"]:
                mycon.rollback()
                print("Transaction rolled back.")
                input("Press Enter to continue...")
                return
            if action not in ["increase","decrease"]:
                print("Invalid action.")
                continue
            item=input("Item name: ").strip()
            if item not in existing:
                print("Item does not exist.")
                continue
            qty=input("Qty change: ").strip()
            if not qty.isdigit():
                print("Enter numeric quantity.")
                continue
            qty=int(qty)
            if action=="decrease":
                qty=-qty
            cur.execute("update inventory set qty=qty+%s where name=%s",(qty,item))
            print("Queued update applied. Commit or continue editing.")

    except Exception as exc:
        mycon.rollback()
        print(f"Batch transaction failed: {exc}")
        input("Press Enter to continue...")

def edit_inventory_items():
    while True:
        clear()
        print("=============== INVENTORY ===============")
        items=fetch_inventory()
        if not items:
            print("Inventory is empty.")
            input("Press Enter to return...")
            return
        display_inventory_list(items)
        print("\nEnter (B) to return to View Inventory")
        field=input("What would you like to edit? (name/price/qty/category/supplier): ").strip().lower()
        if field=="b":
            return
        if field not in {"name","price","qty","category","supplier"}:
            print("Invalid option selected.")
            input("Press Enter to continue...")
            continue

        existing_names=set(fetch_item_names())
        itemname=input("Enter the item to change: ").strip()
        if itemname.lower()=="b":
            continue
        if itemname not in existing_names:
            print("Item does not exist.")
            input("Press Enter to continue...")
            continue

        if field=="name":
            new_value=input("Enter the new name: ").strip()
        elif field=="price":
            while True:
                new_value=input("Enter the new price: ").strip()
                if new_value.isdigit():
                    break
                print("Please enter a valid numeric price.")
        elif field=="qty":
            while True:
                new_value=input("Enter the new quantity: ").strip()
                if new_value.isdigit():
                    break
                print("Please enter a valid quantity.")
        elif field=="category":
            new_value=prompt_category()
        else:  # supplier
            new_value=prompt_supplier_selection()

        column_map={"name":"name","price":"price","qty":"qty","category":"category","supplier":"supplier_id"}
        change=f"update inventory set {column_map[field]}=%s where name=%s"
        cur.execute(change,(new_value,itemname))
        mycon.commit()
        if field=="name":
            existing_names.discard(itemname)
            existing_names.add(new_value)
        print("Data has been changed!")
        if not prompt_yes_no("Would you like to edit anything else? (yes/no): "):
            return

def main():
    clear()
    print("***********************")
    print("       StoreSync")
    print("***********************")
    print("What would you like to do?")
    print("Press 1 : Add items to inventory")
    print("Press 2 : View and Manage inventory")
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
    existing_items=set(fetch_item_names())
    for i in range(1,num+1):
        while True:
            useritem=input("Enter item name: ").strip()
            if useritem and useritem not in existing_items:
                existing_items.add(useritem)
                break 
            print("Item already exists or name is empty.")  
        while True:
            itemprice=input("Price of Item: ").strip()
            if itemprice.isdigit():
                break
            print("Please enter a numeric value for price.")
        while True:
            itemqty=input("Enter qty of item: ").strip()
            if itemqty.isdigit():
                itemqty=int(itemqty)
                break
            print("Please enter a numeric value for quantity.")
        category=prompt_category()
        supplier_id=prompt_supplier_selection()
        insert= "insert into inventory (name,category,price,qty,expdate,supplier_id) values(%s,%s,%s,%s,%s,%s);"
        expiry=shortExpiry if useritem in veg else longExpiry
        insert_tup=(useritem,category,itemprice,itemqty,expiry,supplier_id)
        cur.execute(insert,insert_tup)
        # maintain a default reorder level entry for every new item
        cur.execute("""
            insert into inventory_thresholds(item_name,reorder_level)
            values(%s,%s)
            on duplicate key update reorder_level=values(reorder_level)
        """,(useritem,5))
        mycon.commit()
    if num == 1:
        returntomenu("Item has been successfully added.")
    else:
        returntomenu("Items have been successfully added.")
        
def viewinventory():
    while True:
        clear()
        print("**************")
        print("VIEW INVENTORY")
        print("**************")
        data=fetch_inventory()
        print("*****")
        print("ITEMS")
        print("*****")
        if not data:
            print("Inventory is empty.")
        else:
            for name,category,price,qty,expdate,_,supplier in data:
                print(f"{name} [{category}] | ₹{price} | Qty: {qty} | Supplier: {supplier} | Exp: {expdate}")
        print()
        print("Options:")
        print("Enter (B) to go back")
        print("Enter 1 to edit an item")
        print("Enter 2 to delete an item")
        print("Enter 3 to get item details")
        print("Enter 4 to restock via stored procedure")
        print("Enter 5 for transaction batch mode")
        userinput=input("Enter number corresponding to required action: ").lower()
        if userinput=="1":
            editinventory()
        elif userinput=="2":
            deleteitem()
        elif userinput=="3": 
            show_item_details_flow()
        elif userinput=="4":
            restock_via_procedure()
        elif userinput=="5":
            transaction_batch_mode()
        elif userinput=="b" :
            main()
            return
    
def editinventory():
    while True:
        clear()
        print("*******************")
        print("EDIT INVENTORY ITEM")
        print("*******************")
        print("Options:")
        print("Enter (B) to return to View Inventory")
        print("Enter 1 to edit Item details")
        userinput=input("Choose option: ").lower()
        if userinput=="b":
            return
        if userinput=="1":
            edit_inventory_items()
            return
        print("Invalid option. Please try again.")
        input("Press Enter to continue...")

        
        
def deleteitem():
    clear()
    print("**************************")
    print("DELETE ITEM FROM INVENTORY")
    print("**************************")
    print("ITEM DETAILS")
    print()
    items=fetch_inventory()
    display_inventory_list(items)
    print()
    existing_items=set(fetch_item_names())
    if not existing_items:
        input("Inventory is empty. Press Enter to return...")
        return
    while True:
        itemtodel=input("Enter name of item to be deleted: ")
        if itemtodel in existing_items:
            break
        else:
            print("Error! Item does not exist")

    if prompt_yes_no("Are you sure you want to delete this item? (yes/no): "):
        delstr="delete from inventory where name=%s"
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
setup_sql_assets()

cur.close()
