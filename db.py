import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Menu (id INTEGER PRIMARY KEY, dish text, description text, price float)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Waiter (id INTEGER PRIMARY KEY, name text, age int)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Tablelist (id INTEGER PRIMARY KEY, capacity int)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Orders (id INTEGER PRIMARY KEY, name text, phone text, items text, tableid int, waiterid int)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM Menu")
        rows = self.cur.fetchall()
        return rows

    def insert(self, dish, description, price):
        self.cur.execute("INSERT INTO Menu VALUES (NULL, ?, ?, ?)", (dish, description, price))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM Menu WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, dish, description, price):
        self.cur.execute("UPDATE Menu SET dish = ?, description = ?, price = ? WHERE id = ?", (dish, description, price, id))
        self.conn.commit()

    def fetchwaiter(self):
        self.cur.execute("SELECT * FROM Waiter")
        rows = self.cur.fetchall()
        return rows

    def insertwaiter(self, name, age):
        self.cur.execute("INSERT INTO Waiter VALUES (NULL, ?, ?)", (name, age))
        self.conn.commit()

    def removewaiter(self, id):
        self.cur.execute("DELETE FROM Waiter WHERE id=?", (id,))
        self.conn.commit()

    def updatewaiter(self, id, name, age):
        self.cur.execute("UPDATE Waiter SET name = ?, age = ?, WHERE id = ?", (name, age, id))
        self.conn.commit()

    def fetchtable(self):
        self.cur.execute("SELECT * FROM Tablelist")
        rows = self.cur.fetchall()
        return rows

    def inserttable(self, capacity):
        self.cur.execute("INSERT INTO Tablelist VALUES (NULL, ?)", (capacity,))
        self.conn.commit()

    def removetable(self, id):
        self.cur.execute("DELETE FROM Tablelist WHERE id=?", (id,))
        self.conn.commit()

    def updatetable(self, id, capacity):
        self.cur.execute("UPDATE Tablelist SET capacity = ? WHERE id = ?", (capacity, id))
        self.conn.commit()   

    def fetchorder(self):
        self.cur.execute("SELECT * FROM Orders")
        rows = self.cur.fetchall()
        return rows

    def insertorder(self, id, name, phone, order, table_id, waiter_id):
        self.cur.execute("INSERT INTO Orders VALUES (?, ?, ?, ?, ?, ?)", (id, name, phone, order, table_id, waiter_id))
        self.conn.commit() 

    def updateorder(self, id, name, phone, orderlist):
        self.cur.execute("UPDATE Orders SET name = ?, phone = ?, items = ? WHERE id = ?", (name, phone, orderlist, id))
        self.conn.commit()   

    def __del__(self):
        self.conn.close()
