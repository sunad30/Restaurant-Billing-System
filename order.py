############################################CREATED BY MUHAMMAD HANAN ASGHAR#################################
from tkinter import *
import random
from tkinter import messagebox
from db import Database
from classes import Dish, Order
# Instanciate databse object
db = Database('store.db')

class Bill_App:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1300x700+0+0")
        self.root.maxsize(width = 1280,height = 700)
        self.root.minsize(width = 1280,height = 700)
        self.root.title("Billing Software")
        self.initialize()
        self.create_widgets()
               

    def create_widgets(self):
        self.cus_name = StringVar()
        self.c_phone = StringVar()
        #For Generating Random Bill Numbers
        x = random.randint(1000,9999)
        
        #Seting Value to variable
        #self.c_bill_no.set(str(x))

        self.tax = StringVar()
        self.subtotal = StringVar()
        self.total = StringVar()
        self.service_tax = StringVar()
        self.service_tax_amount = 50
        #===================================
        bg_color = "#074463"
        fg_color = "white"
        lbl_color = 'white'
        #Title of App
        title = Label(self.root,text = "Billing Software",bd = 12,relief = GROOVE,fg = fg_color,bg = bg_color,font=("times new roman",30,"bold"),pady = 3).pack(fill = X)

        #==========Customers Frame==========#
        F1 = LabelFrame(text = "Customer Details",font = ("time new roman",12,"bold"),fg = "gold",bg = bg_color,relief = GROOVE,bd = 10)
        F1.place(x = 0,y = 80,relwidth = 1)

        #===============Customer Name===========#
        cname_lbl = Label(F1,text="Customer Name",bg = bg_color,fg = fg_color,font=("times new roman",15,"bold")).grid(row = 0,column = 0,padx = 10,pady = 5)
        cname_en = Entry(F1,bd = 8,relief = GROOVE,textvariable = self.cus_name)
        cname_en.grid(row = 0,column = 1,ipady = 4,ipadx = 30,pady = 5)

        #=================Customer Phone==============#
        cphon_lbl = Label(F1,text = "Phone No",bg = bg_color,fg = fg_color,font = ("times new roman",15,"bold")).grid(row = 0,column = 2,padx = 20)
        cphon_en = Entry(F1,bd = 8,relief = GROOVE,textvariable = self.c_phone)
        cphon_en.grid(row = 0,column = 3,ipady = 4,ipadx = 30,pady = 5)

        #====================Customer Bill No==================#
        cbill_lbl = Label(F1,text = "Bill No.",bg = bg_color,fg = fg_color,font = ("times new roman",15,"bold"))
        cbill_lbl.grid(row = 0,column = 4,padx = 20)
        self.c_bill_no = StringVar()
        self.c_bill_no.set(self.order_no[0])
        drop_cbill = OptionMenu(F1, self.c_bill_no, *self.order_no)
        drop_cbill.grid(row = 0, column = 5, ipadx = 30,ipady = 4,pady = 5)
        #====================Bill Search Button===============#
        bill_btn = Button(F1,text = "Enter",bd = 7,relief = GROOVE,font = ("times new roman",12,"bold"),bg = bg_color,fg = fg_color)
        bill_btn.grid(row = 0,column = 6,ipady = 5,padx = 60,ipadx = 19,pady = 5)

        #==================Cosmetics Frame=====================#
        F2 = LabelFrame(self.root,text = 'Your Order',bd = 10,relief = GROOVE,bg = bg_color,fg = "gold",font = ("times new roman",13,"bold"))
        F2.place(x = 5,y = 180,width = 325,height = 380)

        #===========Frame Content
        
        self.entries = []
        i = 0
        x = 5
        for dish in self.dishes_list:
            self.entries.append(Entry(F2,bd = 8,relief = GROOVE))
            self.entries[-1].insert(0,0)
            self.entries[-1].grid(row = i, column = 1, ipady = 5,ipadx = 5) 
            lbName = str(dish.getid())
            lbName = Label(F2,font = ("times new roman",15,"bold"),fg = lbl_color,bg = bg_color, text = dish.getname() + ": Rs." + str(dish.getprice()))
            lbName.grid(row = i, column = 0, padx = 10,pady = 20)
            if i == 4:
                i=0
                F2 = LabelFrame(self.root,text = '',bd = 10,relief = GROOVE,bg = bg_color,fg = "gold",font = ("times new roman",13,"bold"))
                F2.place(x = x+325,y = 180,width = 325,height = 380)
            i += 1
    
        
        #===================Bill Aera================#
        F3 = Label(self.root,bd = 10,relief = GROOVE)
        F3.place(x = 960,y = 180,width = 325,height = 380)
        #===========
        bill_title = Label(F3,text = "Bill Area",font = ("Lucida",13,"bold"),bd= 7,relief = GROOVE)
        bill_title.pack(fill = X)

        #============
        scroll_y = Scrollbar(F3,orient = VERTICAL)
        self.txt = Text(F3,yscrollcommand = scroll_y.set)
        scroll_y.pack(side = RIGHT,fill = Y)
        scroll_y.config(command = self.txt.yview)
        self.txt.pack(fill = BOTH,expand = 1)

        #===========Buttons Frame=============#
        F4 = LabelFrame(self.root,text = 'Bill Menu',bd = 10,relief = GROOVE,bg = bg_color,fg = "gold",font = ("times new roman",13,"bold"))
        F4.place(x = 0,y = 560,relwidth = 1,height = 145)

        #===================
        tax_lbl = Label(F4,font = ("times new roman",15,"bold"),fg = lbl_color,bg = bg_color,text = "Tax")
        tax_lbl.grid(row = 0,column = 0,padx = 10,pady = 0)
        tax_en = Entry(F4,bd = 8,relief = GROOVE,textvariable = self.tax)
        tax_en.grid(row = 0,column = 1,ipady = 2,ipadx = 5)

        #===================
        stax_lbl = Label(F4,font = ("times new roman",15,"bold"),fg = lbl_color,bg = bg_color,text = "Service Tax")
        stax_lbl.grid(row = 1,column = 0,padx = 10,pady = 5)
        stax_en = Entry(F4,bd = 8,relief = GROOVE,textvariable = self.service_tax)
        stax_en.grid(row = 1,column = 1,ipady = 2,ipadx = 5)

        #================
        subtotal_lbl = Label(F4,font = ("times new roman",15,"bold"),fg = lbl_color,bg = bg_color,text = "Subtotal")
        subtotal_lbl.grid(row = 0,column = 2,padx = 30,pady = 0)
        subtotal_en = Entry(F4,bd = 8,relief = GROOVE,textvariable = self.subtotal)
        subtotal_en.grid(row = 0,column = 3,ipady = 2,ipadx = 5)

        #=================
        total_lbl = Label(F4,font = ("times new roman",15,"bold"),fg = lbl_color,bg = bg_color,text = "Amount Due")
        total_lbl.grid(row = 1,column = 2,padx = 30,pady = 5)
        total_en = Entry(F4,bd = 8,relief = GROOVE,textvariable = self.total)
        total_en.grid(row = 1,column = 3,ipady = 2,ipadx = 5)

        #====================
        total_btn = Button(F4,text = "Total",bg = bg_color,fg = fg_color,font=("lucida",12,"bold"),bd = 7,relief = GROOVE,command = self.totalfun)
        total_btn.grid(row = 1,column = 4,ipadx = 20,padx = 30)
        #========================
        genbill_btn = Button(F4,text = "Generate Bill",bg = bg_color,fg = fg_color,font=("lucida",12,"bold"),bd = 7,relief = GROOVE,command = self.bill_area)
        genbill_btn.grid(row = 1,column = 5,ipadx = 20)
        #====================
        clear_btn = Button(F4,text = "Clear",bg = bg_color,fg = fg_color,font=("lucida",12,"bold"),bd = 7,relief = GROOVE,command = self.clear)
        clear_btn.grid(row = 1,column = 6,ipadx = 20,padx = 30)
        #======================
        exit_btn = Button(F4,text = "Exit",bg = bg_color,fg = fg_color,font=("lucida",12,"bold"),bd = 7,relief = GROOVE,command = self.exit)
        exit_btn.grid(row = 1,column = 7,ipadx = 20)

    def initialize(self):
        self.dishes_list = []
        for row in db.fetch():
            self.dishes_list.append(Dish(row[0],row[1],row[2],row[3]))
        self.order_list = []
        self.order_no = []
        for row in db.fetchorder():
            self.order_list.append(Order(row[0],row[1],row[2],row[3],row[4],row[5]))    
            self.order_no.append(str(row[0]))

#Function to get total prices
    def totalfun(self):
        self.subtotal_amount = 0
        self.order_desc = ""
        for entry in self.entries:
            amount = self.dishes_list[self.entries.index(entry)].getprice() * float(entry.get())
            self.subtotal_amount += amount
            if int(entry.get())!=0:
                self.order_desc += str(self.entries.index(entry)) + ":" + str(entry.get())+", "
        print(self.order_desc)
        self.subtotal.set("Rs. "+ str(self.subtotal_amount))
        self.tax_amount = round(self.subtotal_amount*0.05)
        self.tax.set("Rs. "+str(self.tax_amount))    
        self.service_tax.set("Rs. "+str(self.service_tax_amount))
        self.total_amount = self.subtotal_amount+self.tax_amount+self.service_tax_amount
        self.total.set("Rs. "+str(self.total_amount))


#Function For Text Area
    def welcome_soft(self):
        self.txt.delete('1.0',END)
        self.txt.insert(END,"       Welcome To Nandos\n")
        self.txt.insert(END,f"\nBill No. : {str(self.c_bill_no.get())}")
        self.txt.insert(END,f"\nCustomer Name : {str(self.cus_name.get())}")
        self.txt.insert(END,f"\nPhone No. : {str(self.c_phone.get())}")
        self.txt.insert(END,"\n===================================")
        self.txt.insert(END,"\nProduct          Qty         Price")
        self.txt.insert(END,"\n===================================")

#Function to clear the bill area
    def clear(self):
        self.txt.delete('1.0',END)

#Add Product name , qty and price to bill area
    def bill_area(self):
        self.welcome_soft()
        for entry in self.entries:
            if int(entry.get())!=0:
                self.txt.insert(END,f"\n{self.dishes_list[self.entries.index(entry)].getname()}\t\t  {entry.get()}\t     {self.dishes_list[self.entries.index(entry)].getprice() * float(entry.get())}")
        self.txt.insert(END,"\n===================================")
        self.txt.insert(END,f"\n                 Subtotal : {self.subtotal_amount}")
        self.txt.insert(END,f"\n                      Tax : {self.tax_amount}")
        self.txt.insert(END,f"\n              Service Tax : {self.service_tax_amount}")
        self.txt.insert(END,f"\n                    Total : {self.total_amount}")
        # Update order
        db.updateorder(int(self.c_bill_no.get()), self.cus_name.get(), self.c_phone.get(), self.order_desc)

    #Function to exit
    def exit(self):
        self.root.destroy()

root = Tk()
object = Bill_App(root)
root.mainloop()