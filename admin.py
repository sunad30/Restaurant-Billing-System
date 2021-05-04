import tkinter as tk
from tkinter import messagebox
from db import Database

# Instanciate databse object
db = Database('store.db')

# Main Application/GUI class


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Restaurant Management - Admin')
        # Width height
        master.geometry("600x900")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()
        self.selected_waiter = 0
        self.populate_waiter()
        self.selected_table = 0
        self.populate_table()

    def create_widgets(self):
        
        # Dishes
        self.dish_text = tk.StringVar()
        self.dish_label = tk.Label(
            self.master, text='Dish Name', font=('bold', 14), pady=20)
        self.dish_label.grid(row=0, column=0, sticky=tk.W)
        self.dish_entry = tk.Entry(self.master, textvariable=self.dish_text)
        self.dish_entry.grid(row=0, column=1)
        
        self.description_text = tk.StringVar()
        self.description_label = tk.Label(
            self.master, text='Description', font=('bold', 14))
        self.description_label.grid(row=0, column=2, sticky=tk.W)
        self.description_entry = tk.Entry(
            self.master, textvariable=self.description_text)
        self.description_entry.grid(row=0, column=3)
        
        self.price_text = tk.DoubleVar()
        self.price_label = tk.Label(
            self.master, text='Price', font=('bold', 14))
        self.price_label.grid(row=1, column=0, sticky=tk.W)
        self.price_entry = tk.Entry(self.master, textvariable=self.price_text)
        self.price_entry.grid(row=1, column=1)
        
        # Waiters
        self.name_text = tk.StringVar()
        self.name_label = tk.Label(
            self.master, text='Waiter Name', font=('bold', 14))
        self.name_label.grid(row=7, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(self.master, textvariable=self.name_text)
        self.name_entry.grid(row=7, column=1)
        
        self.age_text = tk.IntVar()
        self.age_label = tk.Label(
            self.master, text='Age', font=('bold', 14))
        self.age_label.grid(row=7, column=2, sticky=tk.W)
        self.age_entry = tk.Entry(self.master, textvariable=self.age_text)
        self.age_entry.grid(row=7, column=3)
        
        #Tables
        self.capacity_text = tk.IntVar()
        self.capacity_label = tk.Label(
            self.master, text='Capacity', font=('bold', 14))
        self.capacity_label.grid(row=1, column=12, sticky=tk.W)
        self.capacity_entry = tk.Entry(self.master, textvariable=self.capacity_text)
        self.capacity_entry.grid(row=1, column=13)


        # Dishes list (listbox)
        self.dishes_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.dishes_list.grid(row=3, column=0, columnspan=3,
                             rowspan=3, pady=20, padx=20)
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        self.dishes_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.dishes_list.yview)
        self.dishes_list.bind('<<ListboxSelect>>', self.select_item)


        # Waiter list (listbox)
        self.waiter_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.waiter_list.grid(row=9, column=0, columnspan=3,
                             rowspan=3, pady=20, padx=20)
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=9, column=3)
        self.waiter_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.waiter_list.yview)
        self.waiter_list.bind('<<ListboxSelect>>', self.select_waiter)

         # Table list (listbox)
        self.table_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.table_list.grid(row=3, column=12, columnspan=3,
                             rowspan=3, pady=20, padx=20)
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=15)
        self.table_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.table_list.yview)
        self.table_list.bind('<<ListboxSelect>>', self.select_table)


        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add Dish", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Remove Dish", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(
            self.master, text="Update Dish", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.addwaiter_btn = tk.Button(
            self.master, text="Add Waiter", width=12, command=self.add_waiter)
        self.addwaiter_btn.grid(row=8, column=0, pady=20)    

        self.removewaiter_btn = tk.Button(
            self.master, text="Remove Waiter", width=12, command=self.remove_waiter)
        self.removewaiter_btn.grid(row=8, column=1, pady=20)

        self.updatewaiter_btn = tk.Button(
            self.master, text="Update Waiter", width=12, command=self.update_waiter)
        self.updatewaiter_btn.grid(row=8, column=2, pady=20)

        self.addtable_btn = tk.Button(
            self.master, text="Add Table", width=12, command=self.add_table)
        self.addtable_btn.grid(row=2, column=12, pady=20)    

        self.removetable_btn = tk.Button(
            self.master, text="Remove Table", width=12, command=self.remove_table)
        self.removetable_btn.grid(row=2, column=13, pady=20)

        self.updatetable_btn = tk.Button(
            self.master, text="Update Table", width=12, command=self.update_table)
        self.updatetable_btn.grid(row=2, column=14, pady=20)

          
    # Dishes
    def populate_list(self):
        self.dishes_list.delete(0, tk.END)
        for row in db.fetch():
            self.dishes_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.dish_text.get() == '' or self.description_text.get() == '' or self.price_text.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return
        print(self.dish_text.get())
        db.insert(self.dish_text.get(), self.description_text.get(), self.price_text.get())
        self.dishes_list.delete(0, tk.END)
        self.dishes_list.insert(tk.END, (self.dish_text.get(), self.description_text.get(), self.price_text.get()))
        self.clear_text()
        self.populate_list()

    # Runs when item is selected
    def select_item(self, event):
        try:
            index = self.dishes_list.curselection()[0]
            self.selected_item = self.dishes_list.get(index)
            self.dish_entry.delete(0, tk.END)
            self.dish_entry.insert(tk.END, self.selected_item[1])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(tk.END, self.selected_item[2])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, self.selected_item[3])
        except IndexError:
            pass

    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.dish_text.get(), self.description_text.get(), self.price_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.dish_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


    # Waiters
    def populate_waiter(self):
        self.waiter_list.delete(0, tk.END)
        for row in db.fetchwaiter():
            self.waiter_list.insert(tk.END, row)

    def add_waiter(self):
        if self.name_text.get() == '' or self.age_text.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return
        print(self.name_text.get())
        db.insertwaiter(self.name_text.get(), self.age_text.get())
        self.waiter_list.delete(0, tk.END)
        self.waiter_list.insert(tk.END, (self.name_text.get(), self.age_text.get()))
        self.clear_waiter()
        self.populate_waiter()

    def select_waiter(self, event):
        try:
            index = self.waiter_list.curselection()[0]
            self.selected_waiter = self.waiter_list.get(index)
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, self.selected_waiter[1])
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(tk.END, self.selected_waiter[2])
        except IndexError:
            pass

    def remove_waiter(self):
        db.removewaiter(self.selected_waiter[0])
        self.clear_waiter()
        self.populate_waiter()

    def update_waiter(self):
        print(selected_waiter[0])
        db.updatewaiter(self.selected_waiter[0], self.name_text.get(), self.age_text.get())
        self.populate_waiter()

    def clear_waiter(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)


    # Tables
    def populate_table(self):
        self.table_list.delete(0, tk.END)
        for row in db.fetchtable():
            self.table_list.insert(tk.END, row)

    def add_table(self):
        if self.capacity_text.get() == '':
            messagebox.showerror("Required Fields", "Please include all fields")
            return
        print(self.capacity_text.get())
        db.inserttable(self.capacity_text.get())
        self.table_list.delete(0, tk.END)
        self.table_list.insert(tk.END, (self.capacity_text.get()))
        self.clear_table()
        self.populate_table()

    def select_table(self, event):
        try:
            index = self.table_list.curselection()[0]
            self.selected_table = self.table_list.get(index)
            self.capacity_entry.delete(0, tk.END)
            self.capacity_entry.insert(tk.END, self.selected_table[1])
        except IndexError:
            pass

    def remove_table(self):
        db.removetable(self.selected_table[0])
        self.clear_table()
        self.populate_table()

    def update_table(self):
        db.updatetable(self.selected_table[0], self.capacity_text.get())
        self.populate_table()
    
    def clear_table(self):
        self.capacity_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
