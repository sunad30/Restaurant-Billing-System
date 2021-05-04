import subprocess
import tkinter as tk
from tkinter import messagebox
from db import Database
import random
from classes import Dish, Waiter, Table, Order
# Instanciate databse object
db = Database('store.db')

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Restaurant Management')
        master.geometry("900x900")
        self.create_widgets()    
        self.initialize()    
        self.order_count = 0

    def create_widgets(self):
        # Buttons
        self.admin_btn = tk.Button(
            self.master, text="Admin Mode", width=14, command=self.admin_mode)
        self.admin_btn.grid(row=0, column=0, pady=20) 

        self.menu_btn = tk.Button(
            self.master, text="Display Menu", width=14, command=self.display_menu)
        self.menu_btn.grid(row=1, column=0, pady=20) 

        self.assigntable_btn = tk.Button(
            self.master, text="Assign a Table", width=14, command=self.assign_table)
        self.assigntable_btn.grid(row=2, column=0, pady=20)

        self.addorder_btn = tk.Button(
            self.master, text="Add an Order", width=14, command=self.add_order)
        self.addorder_btn.grid(row=3, column=0, pady=20)

        self.orderinfo_btn = tk.Button(
            self.master, text="Display Orders", width=14, command=self.display_order)
        self.orderinfo_btn.grid(row=4, column=0, pady=20)

    def initialize(self):
        self.dishes_list = []
        for row in db.fetch():
            self.dishes_list.append(Dish(row[0],row[1],row[2],row[3]))
        self.tables_list = []
        for row in db.fetchtable():
            self.tables_list.append(Table(row[0],row[1],0))  
        self.waiters_list = []
        for row in db.fetchwaiter():
            self.waiters_list.append(Waiter(row[0],row[1],1))         
        x = random.randint(1000,9999)
        self.cbill_no = tk.StringVar()
        self.cbill_no.set(str(x))

    def admin_mode(self):
        self.password_text = tk.StringVar()
        self.password_label = tk.Label(
            self.master, text='Enter Password', font=('bold', 14))
        self.password_label.grid(row=0, column=2, sticky=tk.W)
        self.password_entry = tk.Entry(self.master, show="*", textvariable=self.password_text)
        self.password_entry.grid(row=0, column=3)
        self.enter_btn = tk.Button(
            self.master, text="Enter", width=10, command=self.authenticate)
        self.enter_btn.grid(row=0, column=4, pady=20) 
        
    def authenticate(self):   
        self.enter_btn.grid_forget()
        self.password_label.grid_forget()
        self.password_entry.grid_forget()
        if self.password_entry.get()=="pass123":   
            subprocess.call(['python', 'admin.py'])
        else: 
            messagebox.showerror("Incorrect Password", "You are not authenticated to open admin mode")
            return

    def display_menu(self):
        self.menu_label = tk.Label(
            self.master, text='Menu', font=(6))
        self.menu_label.grid(row=7, column=0, sticky=tk.W)
        self.dishes_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.dishes_list.grid(row=8, column=0, columnspan=3,
                             rowspan=3, pady=20, padx=20)
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=8, column=3)
        self.dishes_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.dishes_list.yview)
        self.populate_list()

    def populate_list(self):
        self.dishes_list.delete(0, tk.END)
        self.dishes_list.insert(tk.END, ("Id", "Dish", "Description", "Price"))
        for row in db.fetch():
            self.dishes_list.insert(tk.END, row)

    def assign_table(self):
        self.available=[]
        for table in self.tables_list:
            if table.getoccupied()==0:
                option="Table Id:"+str(table.getid())+" Capacity:"+str(table.getcapacity())
                self.available.append(option)
        self.available_waiter=[]
        for waiter in self.waiters_list:
                if waiter.getavailable()==1:
                    option="Waiter Id:"+str(waiter.getid())+" Name:"+str(waiter.getname())
                    self.available_waiter.append(option)
        if self.available==[]:
            messagebox.showerror("No availability", "All tables are occupied")
            return    
        elif self.available_waiter==[]:
            messagebox.showerror("No availability", "All waiters are presently busy")
            return  
        else:
            self.clicked = tk.StringVar()
            self.clicked.set(self.available[0])
            self.drop = tk.OptionMenu(self.master, self.clicked, *self.available)
            self.drop.grid(row=2, column=2)
            self.clicked_waiter = tk.StringVar()
            self.clicked_waiter.set(self.available_waiter[0])
            self.drop_waiter = tk.OptionMenu(self.master, self.clicked_waiter, *self.available_waiter)
            self.drop_waiter.grid(row=2, column=3)
            self.select_btn = tk.Button(
                self.master, text="Assign", width=10, command=self.update_availability)
            self.select_btn.grid(row=2, column=4, pady=20)
            self.cbill_lbl = tk.Label(self.master,text = "Bill No.",font=('bold', 14))
            self.cbill_lbl.grid(row = 3,column = 6)
            self.cbill_en = tk.Entry(self.master, textvariable = self.cbill_no)
            self.cbill_en.grid(row = 3,column = 7)


    def update_availability(self):
        table=self.clicked.get()
        waiter=self.clicked_waiter.get()
        t_id=int(table[9])-1
        self.tables_list[t_id].toggleoccupied()
        w_id=int(waiter[10])-1  
        self.waiters_list[w_id].toggleavailable()
        self.select_btn.grid_forget()
        self.drop.grid_forget()
        self.drop_waiter.grid_forget()
        self.neworder = Order(int(self.cbill_no.get()), "", "", "", t_id, w_id)
        print(self.neworder.id,self.neworder.custname)
        self.cbill_lbl.grid_forget()
        self.cbill_en.grid_forget()
        self.add_order()
        if self.cbill_no.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return
        print(self.cbill_no.get())
        db.insertorder(self.neworder.getid(),"","","",self.neworder.gettid(),self.neworder.getwid())       

    def add_order(self): 
        subprocess.call(['python', 'order.py'])

    def display_order(self):            
        self.order_label = tk.Label(
            self.master, text='Order', font=(6))
        self.order_label.grid(row=7, column=0, sticky=tk.W)
        self.order_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.order_list.grid(row=8, column=0, columnspan=9,
                             rowspan=3, pady=20, padx=20)
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=8, column=9)
        self.order_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.order_list.yview)
        self.populate_order()

    def populate_order(self):
        self.order_list.delete(0, tk.END)
        self.order_list.insert(tk.END, ("Id", "Name", "Items        ", "Table", "Waiter"))
        for row in db.fetchorder():
            self.order_list.insert(tk.END, (row[0],row[1],row[3],row[4],row[5]))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
