import sqlite3

class PersonalSpend:
    def __init__(self):
        # Establish a connection to the SQLite database file
        self.connection = sqlite3.connect("spending.db")
        self.cursor = self.connection.cursor()
        
        # Create the Spend table if it doesn't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Spend (spend REAL, store TEXT,  date TEXT)")
        self.connection.commit()
    
    def show(self):
        # Retrieve the last 10 records from the Spend table
        return self.cursor.execute("SELECT * FROM Spend ORDER BY rowid DESC LIMIT 10").fetchall()

    def add(self, spend, store, date):
        # Insert a new record into the Spend table
        self.cursor.execute("INSERT INTO Spend VALUES (?, ?, ?)", (spend, store, date))
        self.connection.commit()
    
    def delete(self, spend, store, date):
        # Delete a record from the Spend table based on spend, store, and date
        self.cursor.execute("DELETE FROM Spend WHERE spend=? and store=? and date=?", (spend, store, date))
        self.connection.commit()

    def allSpend(self):
        # Retrieve all spend values from the Spend table
        return self.cursor.execute("SELECT spend FROM Spend").fetchall()
    
    def diffDates(self):
        # Retrieve the oldest and newest dates from the Spend table
        new = self.cursor.execute("SELECT date FROM Spend ORDER BY date DESC LIMIT 1").fetchone()
        old = self.cursor.execute("SELECT date FROM Spend ORDER BY date LIMIT 1").fetchone()
        return (old, new)
    
    def updateRow(self, spend, store, date, nSpend, nStore, nDate):
        # Update a row in the Spend table with new values
        self.cursor.execute("UPDATE Spend SET spend=?, store=?, date=? WHERE spend=? and store=? and date=?", (nSpend, nStore, nDate, spend, store, date))
        self.connection.commit()

    def close(self):
        self.connection.close()

class StoreItems:
    def __init__(self):
        # Establish a connection to the SQLite database file
        self.connection = sqlite3.connect("store_items.db")
        self.cursor = self.connection.cursor()

        # Create the Items table if it doesn't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Items (name TEXT, price REAL, quantity INTEGER, category TEXT, storename TEXT)")
        self.connection.commit()
    
    def show(self, name, category, store, order):
        # Construct the SQL query based on the provided parameters
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
        elif order == "(£) Low to High":
            return self.cursor.execute(search + " ORDER BY price LIMIT 21").fetchall()
        elif order == "(£) High to Low":
            return self.cursor.execute(search + " ORDER BY price DESC LIMIT 21").fetchall()
        else:
            return self.cursor.execute(search + " LIMIT 21").fetchall()

    def add(self, name, price, quantity, category, storename):
        # Insert a new record into the Items table
        self.cursor.execute("INSERT INTO Items VALUES (?, ?, ?, ?, ?)", (name, price, quantity, category, storename))
        self.connection.commit()
    
    def delete(self, name, price, quantity, category, storename):
        # Delete a record from the Items table based on the provided values
        self.cursor.execute("DELETE FROM Items WHERE name=? and price=? and quantity=? and category=? and storename=?", (name, price, quantity, category, storename))
        self.connection.commit()

    def close(self):
        self.connection.close()