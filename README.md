# Food-Cash-Processing-Using-Python

In this application Python is used which is linked with MySQL database. Python is an interpreted, high-level, general-purpose programming language. It is developer-friendly language and is more expressive meaning that it is more understandable and readable. Various features of Python make it more useful like it’s free and open source, supports object oriented programming and concepts of classes and objects, it has large standard library, supports in-built GUI and can be easily integrated with languages like C, C++, JAVA etc.

For the proper working of the code you must create database and the tables manually.

Assumptions:-

•	In the CAFE database we have 4 Entities namely ADMIN, FOOD_ITEMS, CUSTOMER and BILL.
•	The ADMIN entity has the following attribute admin_id, name, pswd, address, phnno. Admin_id is the primary key for this entity.
•	The FOOD_ITEMS entity has the following attributes food_id, name, price where food_id is the primary key.
•	The CUSTOMER entity has the following attributes cust_id, name, address, pswd, phnno. Where cust_id is the primary key.
•	The BILL entity has the following attributes bill_no, date, total_amt where bill_no is the primary key.
•	The ordered_by relationship between FOOD_ITEM and CUSTOMER is of cardinality ration M:N i.e. many to many, a customer can order many food items and a food item can be ordered by     many customers.
•	The contains relationship between BILL and FOOD_ITEM is of cardinality ratio M:N i.e. many to many, a bill can contain many food items and a food item can be in many bills.
•	The paid_by relationship between BILL and CUSTOMER  is of cardinality ration 1:1 i.e. one to one, a bill can only be paid by a customer and a customer can pay only one bill at a time.
•	The manages relationship between ADMIN and FOOD_ITEM is of cardinality ration 1:N i.e. one to many, a admin can manage many food items and food items can be managed by a admin at a time.
•	Both ADMIN and FOOD_ITEM are totally participating with each other in manages relationship.
•	Both FOOD_ITEM and CUSTOMER are totally participating with each other in ordered_by relationship.
•	BILL is totally participating with FOOD_ITEM but FOOD_ITEM is partially participating with BILL in the contains relationship.
•	BILL is totally participating with CUSTOMER but CUSTOMER is partially participating with BILL in the paid_by relationship. 

Follow/refer these :

To create ADMIN:
Create table admin (admin_id varchar(10), Name varchar(10), Address varchar(20), Pswd varchar(10), Phnno int(10), constraint pk1 primary key(Admin_id));
To create FOOD_ITEM:
Create table food_item (Food_id varchar(10), Name varchar(10), Price int(5), constraint pk2 primary key(Food_id), admin_id varchar(10),constraint fk1 foreign key(Admin_id) references admin(Admin_id) on delete cascade);
To create CUSTOMER:
Create table customer (Cust_id varchar(10), Name varchar(10), Address varchar(20), Pswd varchar(10), Phnno int(10), constraint pk3 primary key(Cust_id));
To create BILL:
Create table bill (Bill_no int(5),  Date date, Total_amt int(5),  constraint pk4 primary key(Bill_no),cust_id varchar(10),constraint fk2 foreign key(Cust_id) references customer(Cust_id) on delete cascade);
To create ‘ordered_by’:
Create table ordered_by (Food_id varchar(10), Cust_id varchar(10), constraint pk5 primary key(Food_id,Cust_id), constraint fk3 foreign key(Food_id) references food_item(Food_id), constraint fk4 foreign key(Cust_id) references customer(Cust_id) on delete cascade );
To create ‘contains’:
Create table contains (Food_id varchar(10), Bill_no int(5), Quantity int(3), constraint pk7 primary key(Food_id,Bill_no), constraint fk5 foreign key(Food_id) references food_item(Food_id), constraint fk6 foreign key(Bill_no) references bill(Bill_no) on delete cascade );
