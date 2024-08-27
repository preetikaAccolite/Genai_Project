import sqlite3
import random
from datetime import datetime, timedelta
database_name = 'Orders.db'
conn = sqlite3.connect(database_name)
# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the Orders table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS Orders (
#         OrderNo INTEGER PRIMARY KEY,
#         Name TEXT NOT NULL,
#         MobileNumber TEXT NOT NULL,
#         Items TEXT NOT NULL,
#         OrderStatus TEXT NOT NULL,
#         OrderTime DATETIME NOT NULL,
#         DeliveryTime DATETIME,
#         Remarks TEXT
#     )
# ''')
#
# # Generate random data
# names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy"]
# items_list = ["Item1", "Item2", "Item3", "Item4", "Item5"]
# statuses = ["Pending", "Shipped", "Delivered"]
# remarks_list = ["", "Urgent", "Gift", "Delayed", "Handle with care"]
#
# def generate_random_mobile():
#     return f'+1{random.randint(1000000000, 9999999999)}'
#
# def generate_random_datetime(start, end):
#     return start + timedelta(
#         seconds=random.randint(0, int((end - start).total_seconds())))
#
# # Insert 20 random records
# for i in range(20):
#     name = random.choice(names)
#     mobile_number = generate_random_mobile()
#     items = ", ".join(random.sample(items_list, random.randint(1, 3)))
#     order_status = random.choice(statuses)
#     order_time = generate_random_datetime(
#         datetime(2023, 1, 1), datetime(2023, 12, 31))
#     delivery_time = (order_time + timedelta(days=random.randint(1, 7))
#                      if order_status == "Delivered" else None)
#     remarks = random.choice(remarks_list)
#
#     cursor.execute('''
#         INSERT INTO Orders (Name, MobileNumber, Items, OrderStatus, OrderTime, DeliveryTime, Remarks)
#         VALUES (?, ?, ?, ?, ?, ?, ?)
#     ''', (name, mobile_number, items, order_status, order_time, delivery_time, remarks))
#
# # Commit the changes
# conn.commit()
#
# # Close the connection
# conn.close()
#
# print("20 records inserted successfully!")

cursor.execute('SELECT * FROM Orders')
rows = cursor.fetchall()
print('Data in the users table:')
for row in rows:
    print(row)


# Data in the users table:
# (1, 'Alice', '+15260984613', 'Item2, Item5', 'Shipped', '2023-10-08 12:31:33', None, 'Handle with care')
# (2, 'Bob', '+14424262322', 'Item4', 'Shipped', '2023-12-26 01:23:13', None, 'Delayed')
# (3, 'Bob', '+17034247683', 'Item4, Item1, Item5', 'Shipped', '2023-04-26 15:10:44', None, 'Urgent')
# (4, 'Frank', '+15210769369', 'Item2', 'Shipped', '2023-10-10 03:59:21', None, 'Delayed')
# (5, 'Ivan', '+18713127711', 'Item5, Item3', 'Pending', '2023-03-21 10:38:41', None, 'Handle with care')
# (6, 'Bob', '+12635188272', 'Item4, Item2', 'Pending', '2023-07-01 04:37:56', None, 'Gift')
# (7, 'Charlie', '+15583177125', 'Item2, Item3', 'Delivered', '2023-09-29 21:55:53', '2023-09-30 21:55:53', 'Gift')
# (8, 'Diana', '+15271754833', 'Item1', 'Delivered', '2023-12-20 00:03:05', '2023-12-26 00:03:05', 'Handle with care')
# (9, 'Alice', '+11054589845', 'Item2, Item3', 'Shipped', '2023-07-13 18:18:55', None, 'Urgent')
# (10, 'Frank', '+15613123706', 'Item1', 'Shipped', '2023-11-08 04:36:12', None, 'Delayed')
# (11, 'Bob', '+15436108885', 'Item3, Item1', 'Delivered', '2023-11-05 06:21:28', '2023-11-11 06:21:28', 'Gift')
# (12, 'Grace', '+12968668845', 'Item1, Item4', 'Shipped', '2023-11-18 16:04:44', None, 'Urgent')
# (13, 'Alice', '+12866855528', 'Item3, Item1', 'Pending', '2023-12-05 03:31:31', None, 'Handle with care')
# (14, 'Heidi', '+12622993653', 'Item5, Item3', 'Delivered', '2023-06-08 07:03:33', '2023-06-13 07:03:33', 'Gift')
# (15, 'Diana', '+17270009261', 'Item3', 'Delivered', '2023-03-18 07:59:19', '2023-03-19 07:59:19', 'Urgent')
# (16, 'Ivan', '+15781336094', 'Item3, Item2', 'Delivered', '2023-04-04 03:26:39', '2023-04-09 03:26:39', 'Gift')
# (17, 'Judy', '+12156828145', 'Item2, Item5', 'Delivered', '2023-11-30 07:54:36', '2023-12-05 07:54:36', 'Urgent')
# (18, 'Charlie', '+16289208112', 'Item4, Item2', 'Delivered', '2023-10-05 04:04:43', '2023-10-10 04:04:43', '')
# (19, 'Ivan', '+14875830123', 'Item5', 'Delivered', '2023-04-13 00:35:58', '2023-04-18 00:35:58', 'Gift')
# (20, 'Frank', '+13812242823', 'Item1', 'Delivered', '2023-02-07 01:38:50', '2023-02-13 01:38:50', '')
