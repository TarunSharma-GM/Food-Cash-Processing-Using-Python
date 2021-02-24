from tkinter import*
import mysql.connector
from tkinter import messagebox
import random
from tkinter.ttk import Treeview
from datetime import date
import time

fdb = mysql.connector.connect(host="localhost", user="root", passwd="tiger", database="testing1")
obj = fdb.cursor()
obj1 = fdb.cursor()
obj2 = fdb.cursor()
obj3 = fdb.cursor(buffered=True)
obj4 = fdb.cursor(buffered=True)


#---------- WELCOME PAGE --------------------
welcome = Tk()
welcome.geometry("500x300+380+190")
welcome.title("FOOD PROCESSING")
Label(welcome, font=('aria', 30, 'bold'), text="Food Cash Processing", fg="Black", bd=10).grid(row=2, column=1)
Label(welcome, font=('aria', 15, 'bold'), text="We welcome you to our Dhaba.", fg="Black", bd=10).grid(row=4, column=1)
Label(welcome, font=('aria', 15, 'bold'), text="Login accordingly.", fg="Black", bd=10).grid(row=6, column=1)

#----------------MENU------------------
def fmenu():
    #import menu
    menu = Tk()
    menu.geometry("600x250+200+50")
    menu.title("ADMIN LOGIN")

    tree = Treeview(menu, columns=('food_id', 'name', 'price'))
    tree.heading('food_id', text='Food Id')
    tree.heading('name', text='Name')
    tree.heading('price', text='Price')
    tree.column("food_id")
    tree.column("name")
    tree.column("price")
    tree.grid()
    tree['show'] = 'headings'

    obj2.execute("SELECT food_id,name,price FROM food_item ")
    fetch = obj2.fetchall()
    for data in fetch:
        tree.insert('', '0', values=(data))


    menu.mainloop()
    obj2.close()
    fdb.close()




#----------ADMIN LOGIN PAGE-------------------
def admin1():
    admin = Tk()
    admin.geometry("800x600+200+50")
    admin.title("ADMIN LOGIN")

    aid = StringVar(admin)
    apd = StringVar(admin)

    Label(admin, font=('aria', 20, 'bold'), text="Login Here To Manage Food Menu", fg="Black", bd=10).grid(row=2, column=1)
    Label(admin, font=('aria', 15), text="ADMIN ID", fg="Black", bd=10).grid(row=4, column=1)
    Entry(admin, textvar=aid).grid(row=4, column=3)
    Label(admin, font=('aria', 15), text="PASSWORD", fg="Black", bd=10).grid(row=6, column=1)
    Entry(admin, textvar=apd, show = "*").grid(row=6, column=3)

    def admlogin():
        #import adminlogin
        adminlogin = Tk()
        adminlogin.geometry("400x450+300+150")
        adminlogin.title("FOOD ORDER MANAGER")

        fid = StringVar(adminlogin)
        fname = StringVar(adminlogin)
        fprice = StringVar(adminlogin)



        Label(adminlogin, font=('aria', 20, 'bold'), text="Welcome Admin ", fg="Black", bd=10).place(x=70, y=0)
        Label(adminlogin, font=('aria', 18), text=" Choose Accordingly ", fg="Black", bd=10).place(x=60, y=70)
        Button(adminlogin, text='FOOD MENU', command=fmenu).place(x=150, y=120)
        Label(adminlogin, font=('aria', 10), text=" Food ID ", fg="Black", bd=10).place(x=25, y=180)
        Entry(adminlogin, textvar=fid, width=12).place(x=30, y=210)
        Label(adminlogin, font=('aria', 10), text=" Name ", fg="Black", bd=10).place(x=25, y=240)
        Entry(adminlogin, textvar=fname, width=12).place(x=30, y=270)
        Label(adminlogin, font=('aria', 10), text=" Price ", fg="Black", bd=10).place(x=25, y=300)
        Entry(adminlogin, textvar=fprice, width=12).place(x=30, y=330)

        Label(adminlogin, font=('aria', 10), text=" Food ID ", fg="Black", bd=10).place(x=145, y=300)
        Entry(adminlogin, textvar=fid, width=12).place(x=140, y=330)

        Label(adminlogin, font=('aria', 10), text=" Food ID ", fg="Black", bd=10).place(x=270, y=240)
        Entry(adminlogin, textvar=fid, width=12).place(x=265, y=270)
        Label(adminlogin, font=('aria', 10), text=" Price ", fg="Black", bd=10).place(x=270, y=300)
        Entry(adminlogin, textvar=fprice, width=12).place(x=265, y=330)

        def fadd():
            if obj1.fetchone() is None:
                obj1.execute("INSERT INTO food_item (food_id, name, price, admin_id) VALUES(%s, %s, %s, %s)",
                             (fid.get(), fname.get(), fprice.get(), aid.get()))
                fdb.commit()
                messagebox.showinfo("Added", "Added Successfully")
            else:
                messagebox.showinfo("Unsuccessful")

        Button(adminlogin, text='ADD', command=fadd).place(x=50, y=380)

        def delt():
            if obj1.fetchone() is None:
                del_stat = "DELETE FROM food_item WHERE food_id = %s " % fid.get()
                obj1.execute(del_stat)
                fdb.commit()
                messagebox.showinfo("DLELETED", "Deleted Successfully")

        Button(adminlogin, text='DELETE', command=delt).place(x=150, y=380)

        def updt():
            if obj1.fetchone() is None:
                obj1.execute("update food_item set price=%s where food_id=%s", (fprice.get(), fid.get()))
                fdb.commit()
                messagebox.showinfo("UPDATED", "New Price Updated")

        Button(adminlogin, text='UPDATE', command=updt).place(x=270, y=380)
        adminlogin.mainloop()

    def checkpswd(event=None):
        print("hello")
        if aid.get() == "" or apd.get() == "":
            print("empty field")
            #admin.config(text="Please complete the required field!", fg="red")
        else:
            obj.execute("SELECT * FROM admin WHERE admin_id = %s AND pswd = %s",(aid.get(), apd.get()))
            print("hi")
            if obj.fetchone() is not None:
                admlogin()
                aid.set("")
                apd.set("")
            else:
                print("Invalid input")
                #admin.config(text="Invalid username or password", fg="red")
        obj.close()
        fdb.close()



    Button(admin, text='LOGIN', command=checkpswd).grid(row=8, column=3)




Button(welcome, text='ADMIN', command=admin1).grid(row=8, column=1)



#------------FOOD ORDERING PAGE AFTER CUSTOMER LOGIN----------------
def ordr(cust_id):
    #import billg
    order = Tk()
    order.geometry("850x600+200+50")
    order.title("FOOD ORDERING")

    itm1fdid = IntVar(order)
    itm1qty = IntVar(order)
    itm1prc = IntVar(order)
    itm2fdid = IntVar(order)
    itm2qty = IntVar(order)
    itm2prc = IntVar(order)
    itm3fdid = IntVar(order)
    itm3qty = IntVar(order)
    itm3prc = IntVar(order)
    itm4fdid = IntVar(order)
    itm4qty = IntVar(order)
    itm4prc = IntVar(order)
    itm5fdid = IntVar(order)
    itm5qty = IntVar(order)
    itm5prc = IntVar(order)
    ttlamt = DoubleVar(order)
    tqty = IntVar(order)
    rand = IntVar(order)
    tdate = date.today()

    def close_window():
        order.destroy()

    def sett():
        itm1fdid.set(0)
        itm1qty.set(0)
        itm2fdid.set(0)
        itm2qty.set(0)
        itm3fdid.set(0)
        itm3qty.set(0)
        itm4fdid.set(0)
        itm4qty.set(0)
        itm5fdid.set(0)
        itm5qty.set(0)

    def cal():
        tqty.set(itm1qty.get() + itm2qty.get() + itm3qty.get() + itm4qty.get() + itm5qty.get())
        print(tqty.get())
        ttlamt.set((itm1qty.get() * itm1prc.get()) + (itm2qty.get() * itm2prc.get()) + (itm3qty.get() * itm3prc.get()) + (
                        itm4qty.get() * itm4prc.get()) + (itm5qty.get() * itm5prc.get()))
        print(ttlamt.get())


        if obj.fetchone() is None:
            obj.execute("INSERT INTO bill (bill_no,date,total_amt,cust_id) VALUES(%s,%s,%s,%s)", (rand.get(), tdate, ttlamt.get(),cust_id.get()))
            fdb.commit()

        else:
            print("Unsuccessful")

        print("CID IS ::::", cust_id.get())
        localtime =time.localtime(time.time())
        print(localtime)

        if itm1fdid.get() != 0 and itm1qty.get() != 0:
            obj3.execute("INSERT INTO contains(food_id,bill_no,quantity) VALUES(%s,%s,%s)",
                         (itm1fdid.get(), rand.get(), itm1qty.get()))
            obj4.execute("INSERT INTO ordered_by(food_id,cust_id,dtime) VALUES(%s,%s,%s)",
                         (itm1fdid.get(),cust_id.get(),localtime))
            fdb.commit()
        if itm2fdid.get() != 0 and itm2qty.get() != 0:
            obj3.execute("INSERT INTO contains(food_id,bill_no,quantity) VALUES(%s,%s,%s)",
                         (itm2fdid.get(), rand.get(), itm2qty.get()))
            obj4.execute("INSERT INTO ordered_by(food_id,cust_id,dtime) VALUES(%s,%s,%s)",
                         (itm2fdid.get(), cust_id.get(), localtime))
            fdb.commit()
        if itm3fdid.get() != 0 and itm3qty.get() != 0:
            obj3.execute("INSERT INTO contains(food_id,bill_no,quantity) VALUES(%s,%s,%s)",
                         (itm3fdid.get(), rand.get(), itm3qty.get()))
            obj4.execute("INSERT INTO ordered_by(food_id,cust_id,dtime) VALUES(%s,%s,%s)",
                         (itm3fdid.get(), cust_id.get(), localtime))
            fdb.commit()
        if itm4fdid.get() != 0 and itm4qty.get() != 0:
            obj3.execute("INSERT INTO contains(food_id,bill_no,quantity) VALUES(%s,%s,%s)",
                         (itm4fdid.get(), rand.get(), itm4qty.get()))
            obj4.execute("INSERT INTO ordered_by(food_id,cust_id,dtime) VALUES(%s,%s,%s)",
                         (itm4fdid.get(), cust_id.get(), localtime))
            fdb.commit()
        if itm5fdid.get() != 0 and itm5qty.get() != 0:
            obj3.execute("INSERT INTO contains(food_id,bill_no,quantity) VALUES(%s,%s,%s)",
                         (itm5fdid.get(), rand.get(), itm5qty.get()))
            obj4.execute("INSERT INTO ordered_by(food_id,cust_id,dtime) VALUES(%s,%s,%s)",
                         (itm5fdid.get(), cust_id.get(), localtime))
            fdb.commit()
        sett()



    def bill_no(event=None):
        x = random.randint(12980, 50876)
        randomRef = int(x)
        rand.set(randomRef)
        print(rand.get())

        if rand.get() == "":
            print("empty field")
        else:
            obj.execute("SELECT * FROM bill WHERE bill_no = '%s' ", (rand.get()))
            print("hi")
            if obj.fetchone() is None:
                cal()
            else:
                bill_no()

    def gbill():
        genbill = Tk()
        genbill.geometry("400x300+200+50")
        genbill.title("BILL")

        # if obj.fetchone() is None:
        if itm1fdid.get() != 0 and itm1qty.get() != 0:
            obj.execute("select price from food_item where food_id= '%s'" % itm1fdid.get())
            fetch1 = obj.fetchone()
            for data1 in fetch1:
                itm1prc.set(data1)
        else:
            print("YOUR CART IS EMPTY")
            itm1prc.set(0)
            itm1qty.set(0)

        if itm2fdid.get() != 0 and itm2qty.get() != 0:
            obj.execute("select price from food_item where food_id= '%s'" % itm2fdid.get())
            fetch2 = obj.fetchone()
            for data2 in fetch2:
                itm2prc.set(data2)
        else:
            itm2prc.set(0)
            itm2qty.set(0)
        if itm3fdid.get() != 0 and itm3qty.get() != 0:
            obj.execute("select price from food_item where food_id= '%s'" % itm3fdid.get())
            fetch3 = obj.fetchone()
            for data3 in fetch3:
                itm3prc.set(data3)
        else:
            itm3prc.set(0)
            itm3qty.set(0)
        if itm4fdid.get() != 0 and itm4qty.get() != 0:
            obj.execute("select price from food_item where food_id= '%s'" % itm4fdid.get())
            fetch4 = obj.fetchone()
            for data4 in fetch4:
                itm4prc.set(data4)
        else:
            itm4prc.set(0)
            itm4qty.set(0)
        if itm5fdid.get() != 0 and itm5qty.get() != 0:
            obj.execute("select price from food_item where food_id= '%s'" % itm5fdid.get())
            fetch5 = obj.fetchone()
            for data5 in fetch5:
                itm5prc.set(data5)
        else:
            itm5prc.set(0)
            itm5qty.set(0)

        bill_no()
        Label(genbill, font=('aria', 20, 'bold'), text="****BILL****", fg="Black", bd=10).place(x=110, y=10)
        Label(genbill, font=('aria', 15, 'bold'), text="DATE : ", fg="blue", bd=10).place(x=20, y=50)
        Label(genbill, font=('aria', 15, 'bold'), text=tdate, fg="blue", bd=10).place(x=250, y=50)
        Label(genbill, font=('aria', 15, 'bold'), text="BILL NO. : ", fg="blue", bd=10).place(x=20, y=90)
        Label(genbill, font=('aria', 15, 'bold'), text=rand.get(), fg="blue", bd=10).place(x=250, y=90)
        Label(genbill, font=('aria', 15, 'bold'), text="TOTAL AMOUNT : ", fg="blue", bd=10).place(x=20, y=130)
        Label(genbill, font=('aria', 15, 'bold'), text=ttlamt.get(), fg="blue", bd=10).place(x=250, y=130)
        Label(genbill, font=('aria', 15, 'bold'), text="CUST ID : ", fg="blue", bd=10).place(x=20, y=170)
        Label(genbill, font=('aria', 15, 'bold'), text=cust_id.get(), fg="blue", bd=10).place(x=250, y=170)



    Label(order, font=('aria', 20, 'bold'), text="Add Food To Cart", fg="Black", bd=10).grid(row=0, column=1)
    Label(order, font=('aria', 15, 'bold'), text="Items", fg="blue", bd=10).grid(row=1, column=1)
    Label(order, font=('aria', 15, 'bold'), text="Food ID", fg="blue", bd=10).grid(row=1, column=2)
    Label(order, font=('aria', 15, 'bold'), text="Quantity", fg="blue", bd=10).grid(row=1, column=3)
    Label(order, font=('aria', 15, 'bold'), text="Item 1", fg="blue", bd=10).grid(row=2, column=1)
    Entry(order, bd=5, textvar=itm1fdid).grid(row=2, column=2)
    Entry(order, bd=5, textvar=itm1qty).grid(row=2, column=3)
    Label(order, font=('aria', 15, 'bold'), text="Item 2", fg="blue", bd=10).grid(row=3, column=1)
    Entry(order, bd=5, textvar=itm2fdid).grid(row=3, column=2)
    Entry(order, bd=5, textvar=itm2qty).grid(row=3, column=3)
    Label(order, font=('aria', 15, 'bold'), text="Item 3", fg="blue", bd=10).grid(row=4, column=1)
    Entry(order, bd=5, textvar=itm3fdid).grid(row=4, column=2)
    Entry(order, bd=5, textvar=itm3qty).grid(row=4, column=3)
    Label(order, font=('aria', 15, 'bold'), text="Item 4", fg="blue", bd=10).grid(row=5, column=1)
    Entry(order, bd=5, textvar=itm4fdid).grid(row=5, column=2)
    Entry(order, bd=5, textvar=itm4qty).grid(row=5, column=3)
    Label(order, font=('aria', 15, 'bold'), text="Item 5", fg="blue", bd=10).grid(row=6, column=1)
    Entry(order, bd=5, textvar=itm5fdid).grid(row=6, column=2)
    Entry(order, bd=5, textvar=itm5qty).grid(row=6, column=3)

    Button(order, text="RESET", command=sett).grid(row=8, column=1)
    Button(order, text="GENERATE BILL", command=gbill).grid(row=8, column=2)
    Button(order, text="EXIT", command=close_window).grid(row=8, column=3)
    Button(order, text="FOOD MENU", command=fmenu).grid(row=1, column=4)

    order.mainloop()


#----------CUSTOMER LOGIN PAGE-------------------
def cust():
    customer = Tk()
    customer.geometry("800x600+200+50")
    customer.title("CUSTOMER LOGIN")

    cust_id = StringVar(customer)
    cpd = StringVar(customer)
    cn = StringVar(customer)
    cp = StringVar(customer)
    ca = StringVar(customer)
    cc = StringVar(customer)

    Label(customer, font=('aria', 20, 'bold'), text="Login Here To Order Food", fg="Black", bd=10).grid(row=0, column=1)
    Label(customer, font=('aria', 15), text="CUSTOMER ID", fg="Black", bd=10).grid(row=2, column=1)
    Entry(customer,textvar=cust_id).grid(row=2, column=2)
    Label(customer, font=('aria', 8), text="(use your phone number as customer id)", fg="Black", bd=10).grid(row=2, column=3)
    Label(customer, font=('aria', 15), text="PASSWORD", fg="Black", bd=10).grid(row=4, column=1)
    Entry(customer, textvar=cpd, show = "*").grid(row=4, column=2)

    def custpswd(event=None):
        print("hello")
        if cust_id.get() == "" or cpd.get() == "":
            print("empty field")
            #admin.config(text="Please complete the required field!", fg="red")
        else:
            obj.execute("SELECT * FROM customer WHERE cust_id = %s AND pswd = %s",(cust_id.get(), cpd.get()))
            print("hi")
            if obj.fetchone() is not None:
                ordr(cust_id)
                cust_id.set("")
                cpd.set("")
            else:
                print("Invalid input")
                #admin.config(text="Invalid username or password", fg="red")
        obj.close()
        fdb.close()

    Button(customer, text='LOGIN', command=custpswd).grid(row=5, column=2)

    Label(customer, font=('aria', 20, 'bold'), text="New Customer, Register Here:", fg="Black", bd=10).grid(row=8, column=1)
    Label(customer, font=('aria', 15), text="Name", fg="Black", bd=10).grid(row=9, column=1)
    Entry(customer, textvar=cn).grid(row=9, column=2)
    Label(customer, font=('aria', 15), text="Phone No.", fg="Black", bd=10).grid(row=10, column=1)
    Entry(customer, textvar=cp).grid(row=10, column=2)
    Label(customer, font=('aria', 15), text="Address", fg="Black", bd=10).grid(row=11, column=1)
    Entry(customer, textvar=ca).grid(row=11, column=2)
    Label(customer, font=('aria', 15), text="Password", fg="Black", bd=10).grid(row=12, column=1)
    Entry(customer, textvar=cc).grid(row=12, column=2)



    def register():
        if obj.fetchone() is None:
            obj.execute("INSERT INTO customer (cust_id, name, address, pswd) VALUES(%s, %s, %s, %s)",(cp.get(),cn.get(),ca.get(),cc.get()))
            fdb.commit()
            messagebox.showinfo("Registered Successfully", "Now you can login.")
        else:
            print("Unsuccessful")

    Button(customer, text='SIGN-UP', command=register).grid(row=13, column=2)

    customer.mainloop()

Button(welcome, text='CUSTOMER', command=cust).grid(row=9, column=1)

welcome.mainloop()