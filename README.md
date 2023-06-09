# Simple Store Insights
Database system for searching item price and checking personal spending.

## Guidelines to setup

### Prerequisites

- Python should be installed: `Python version >= 3.9.6`

### Run the APP
```
python <file_path>/main.py
```

## DEMO Images

<img src="/demo/main-screen.png" width=340px /><img src="/demo/delete-item.png" width=340px />
<img src="/demo/spend-screen.png" width=340px /><img src="/demo/edit-popup.png" width=340px />
<img src="/demo/edit-screen.png" width=340px />

#### `PersonalSpend` class:

> **Note**
> The PersonalSpend class is responsible for managing personal spending data.

+ The `__init__` method initializes the class by establishing a connection to the "spending.db" SQLite database and creating a cursor object to execute SQL queries.
+ The `show` method retrieves the last 10 entries from the "Spend" table, ordered by the row id (the auto-incremented row identifier) in descending order.
+ The `add` method adds a new spending entry to the "Spend" table with the provided spend, store, and date values.
+ The `delete` method removes a specific spending entry from the "Spend" table based on the provided spend, store, and date values.
+ The `allSpend` method retrieves all spending values from the "Spend" table.
+ The `diffDates` method retrieves the oldest and newest dates from the "Spend" table.
+ The `updateRow` method updates a specific spending entry in the "Spend" table with new spend, store, and date values.
+ The `close` method closes the database connection.


#### `StoreItems` class:

> **Note**
> The StoreItems class handles the management of store items data.

+ The `__init__` method initializes the class by establishing a connection to the "store_items.db" SQLite database and creating a cursor object to execute SQL queries.
+ The `show` method retrieves store item records from the "Items" table based on the provided name, category, store, and order parameters. The SQL query is constructed dynamically based on the provided values.
+ The `add` method adds a new store item record to the "Items" table with the provided name, price, quantity, category, and storename values.
+ The `delete` method removes a specific store item record from the "Items" table based on the provided name, price, quantity, category, and storename values.
+ The `close` method closes the database connection.


