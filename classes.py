class Dish:
    def __init__(self, id, name, description, price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

    def getid(self):
        return self.id

    def getname(self):
        return self.name

    def getprice(self):
        return self.price


class Waiter:
    def __init__(self, id, name, available):
        self.id = id
        self.name = name
        self.available = available

    def getid(self):
        return self.id

    def getname(self):
        return self.name

    def getavailable(self):
        return self.available

    def toggleavailable(self):
        self.available = not self.available


class Table:
    def __init__(self, id, capacity, occupied):
        self.id = id
        self.capacity = capacity
        self.occupied = occupied

    def getid(self):
        return self.id

    def getcapacity(self):
        return self.capacity

    def getoccupied(self):
        return self.occupied  

    def toggleoccupied(self):
        self.occupied = not self.occupied    


class Order:
    def __init__(self, id, custname, phoneno, items, table_id, waiter_id):
        self.id = id
        self.custname = custname
        self.phoneno = phoneno
        self.items = items
        self.table_id = table_id
        self.waiter_id = waiter_id

    def getid(self):
        return self.id

    def gettid(self):
        return self.table_id

    def getwid(self):
        return self.waiter_id