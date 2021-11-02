import sqlite3

# connection = sqlite3.connect("spending.db")
# cursor = connection.cursor()
# cursor.execute("CREATE TABLE Spend (spend REAL, store TEXT,  date TEXT)")
# connection.commit()
# connection = sqlite3.connect("itemInfo.db")
# cursor = connection.cursor()
# cursor.execute("CREATE TABLE Items (name TEXT, price REAL, quantity INTEGER, category TEXT, storename TEXT)")
# connection.commit()

class Spend:
    def __init__(self):
        self.connection = sqlite3.connect("spending.db")
        self.cursor = self.connection.cursor()
    
    def show(self):
        return self.cursor.execute("SELECT * FROM Spend ORDER BY rowid DESC LIMIT 10").fetchall()

    def add(self, spend, store, date):
        self.cursor.execute("INSERT INTO Spend VALUES (?, ?, ?)", (spend, store, date))
        self.connection.commit()
    
    def delete(self, spend, store, date):
        self.cursor.execute("DELETE FROM Spend WHERE spend=? and store=? and date=?", (spend, store, date))
        self.connection.commit()

    def allSpend(self):
        return self.cursor.execute("SELECT spend FROM Spend").fetchall()
    
    def diffDates(self):
        new = self.cursor.execute("SELECT date FROM Spend ORDER BY date DESC LIMIT 1").fetchone()
        old = self.cursor.execute("SELECT date FROM Spend ORDER BY date LIMIT 1").fetchone()
        return (old, new)
    
    def updateRow(self, spend, store, date, nSpend, nStore, nDate):
        self.cursor.execute("UPDATE Spend SET spend=?, store=?, date=? WHERE spend=? and store=? and date=?", (nSpend, nStore, nDate, spend, store, date))
        self.connection.commit()

class Items:
    def __init__(self):
        self.connection = sqlite3.connect("itemInfo.db")
        self.cursor = self.connection.cursor()
    
    def show(self, name, category, store, order):
        search = f"SELECT * FROM Items WHERE LOWER(name) LIKE LOWER('%{name}%')"
        if category != "Filter Category":
            search += f" and category='{category}'"
        if store != "Filter Stores":
            if store == "Sainsbury's":
                search += f" and storename LIKE '{store[:-2]}%'"
            else:
                search += f" and storename='{store}'"
        if category == "Filter Category" and store == "Filter Stores" and order == "Order By":
            return self.cursor.execute(search + " ORDER BY rowid DESC LIMIT 21").fetchall()
        elif order == "Alphabet":
            return self.cursor.execute(search +" ORDER BY LOWER(name) LIMIT 21").fetchall()
        elif order == "Low to High":
            return self.cursor.execute(search + " ORDER BY price LIMIT 21").fetchall()
        elif order == "High to Low":
            return self.cursor.execute(search + " ORDER BY price DESC LIMIT 21").fetchall()
        else:
            return self.cursor.execute(search + " LIMIT 21").fetchall()

    def add(self, name, price, quantity, category, storename):
        self.cursor.execute("INSERT INTO Items VALUES (?, ?, ?, ?, ?)", (name, price, quantity, category, storename))
        self.connection.commit()
    
    def delete(self, name, price, quantity, category, storename):
        self.cursor.execute("DELETE FROM Items WHERE name=? and price=? and quantity=? and category=? and storename=?", (name, price, quantity, category, storename))
        self.connection.commit()