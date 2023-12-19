# Description: This script initializes the SQLite database and populates it with demo data.

import sqlite3

# Initialize the SQLite database connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Read and execute the schema script from the file
with open('schema.sql', 'r') as schema_file:
    schema_script = schema_file.read()
cursor.executescript(schema_script)

# Insert demo data into the database
# Insert Users
cursor.execute("INSERT INTO Users (username, password_hash, user_type, email, contact_number) VALUES ('amirah123', 'hash1', 'customer', 'amirah@example.com', '+973-12345678')")
cursor.execute("INSERT INTO Users (username, password_hash, user_type, email, contact_number) VALUES ('yahya456', 'hash2', 'customer', 'yahya@example.com', '+973-12322678')")
cursor.execute("INSERT INTO Users (username, password_hash, user_type, email, contact_number) VALUES ('noura789', 'hash3', 'staff', 'noura@example.com', '+973-12345128')")
cursor.execute("INSERT INTO Users (username, password_hash, user_type, email, contact_number) VALUES ('fahad321', 'hash4', 'staff', 'fahad@example.com', '+973-11945678')")

# Insert Customer Data
cursor.execute("INSERT INTO CustomerData (user_id, name, address) VALUES (1, 'Amirah Al-Sayed', 'Manama, Bahrain')")
cursor.execute("INSERT INTO CustomerData (user_id, name, address) VALUES (2, 'Yahya Al-Dossary', 'Riffa, Bahrain')")

# Insert Staff Data
cursor.execute("INSERT INTO StaffData (user_id, name, position, date_of_join) VALUES (3, 'Noura Al Khalifa', 'Pharmacist', '2015-03-01')")
cursor.execute("INSERT INTO StaffData (user_id, name, position, date_of_join) VALUES (4, 'Fahad Al-Shirawi', 'Manager', '2012-07-15')")

# Insert Products
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Paracetamol', 'Pain reliever and fever reducer', 'Generic Pharma Co.', '2024-08-01', 5.99, 100)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Amoxicillin', 'Antibiotic', 'Medicure Labs', '2025-01-15', 12.50, 80)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Ibuprofen', 'Anti-inflammatory drug', 'HealthPlus Inc.', '2023-12-10', 7.25, 150)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Aspirin', 'Pain reliever and fever reducer', 'Generic Pharma Co.', '2024-08-01', 5.99, 100)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Ciprofloxacin', 'Antibiotic', 'Medicure Labs', '2025-01-15', 12.50, 80)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Naproxen', 'Anti-inflammatory drug', 'HealthPlus Inc.', '2023-12-10', 7.25, 150)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Acetaminophen', 'Pain reliever and fever reducer', 'Generic Pharma Co.', '2024-08-01', 5.99, 100)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Cephalexin', 'Antibiotic', 'Medicure Labs', '2025-01-15', 12.50, 80)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Celecoxib', 'Anti-inflammatory drug', 'HealthPlus Inc.', '2023-12-10', 7.25, 150)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Cetirizine', 'Allergy relief medication', 'AllergyCare Ltd.', '2025-03-17', 7.40, 120)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Multivitamins', 'General wellness and health supplement', 'VitaHealth', '2025-12-31', 10.50, 200)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Loratadine', 'Treats allergies and hay fever', 'Allergy Solutions', '2024-08-24', 5.30, 100)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Simvastatin', 'Lowers cholesterol and triglycerides', 'HeartCare Pharmaceuticals', '2025-09-15', 14.00, 60)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Metformin', 'Manages blood sugar levels', 'Diabetes Health Inc.', '2024-07-20', 8.99, 90)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Amlodipine', 'Blood pressure medication', 'CardioPharma', '2025-10-10', 11.75, 70)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Lipitor', 'Cholesterol lowering medication', 'HealthyHeart Ltd.', '2025-04-30', 15.25, 50)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Glucophage', 'Diabetes medication', 'Wellness Pharma', '2024-03-22', 9.60, 85)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Plavix', 'Prevents blood clots', 'BloodCare Meds', '2025-06-18', 17.50, 75)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Advil', 'Pain relief medication', 'Advil Pharma', '2024-05-01', 6.99, 100)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Zyrtec', 'Allergy relief medication', 'AllergyCare Ltd.', '2025-03-17', 7.40, 120)")
cursor.execute("INSERT INTO Products (name, description, supplier, expiry_date, price, quantity_in_stock) VALUES ('Centrum', 'General wellness and health supplement', 'VitaHealth', '2025-12-31', 10.50, 200)")

# Insert Orders
cursor.execute("INSERT INTO Orders (user_id, order_date, total_amount) VALUES (1, '2023-12-01', 43.95)")
cursor.execute("INSERT INTO Orders (user_id, order_date, total_amount) VALUES (1, '2023-12-03', 15.70)")
cursor.execute("INSERT INTO Orders (user_id, order_date, total_amount) VALUES (2, '2023-12-04', 22.15)")

# Insert Order Details
cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (1, 1, 2, 12.50)")
cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (1, 2, 1, 5.99)")
cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (1, 3, 1, 5.99)")
cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (2, 4, 3, 7.25)")
cursor.execute("INSERT INTO OrderDetails (order_id, product_id, quantity, price) VALUES (3, 5, 1, 4.80)")

# Commit the changes to the database
conn.commit()

# Close the database connection
conn.close()

print("Database initialized and demo data populated successfully.")
