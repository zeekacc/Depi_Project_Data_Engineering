import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

server = 'DESKTOP-BIKQPHC'
database = 'LaptopDB'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

conn = pyodbc.connect(conn_str)

query = """
SELECT 
    p.ProductID, 
    p.ProductName, 
    pd.CPUModel, 
    pd.CPUFreq, 
    pd.Ram, 
    pd.Inches, 
    pd.Price,
    f.SaleDate, 
    f.QuantitySold, 
    f.TotalAmount
FROM 
    Product p
JOIN 
    ProductDetails pd ON p.ProductID = pd.ProductID
JOIN 
    FactSales f ON pd.DetailID = f.DetailID;
"""

product_sales_data = pd.read_sql(query, conn)

# Top-selling Products by Quantity
top_selling_by_quantity = product_sales_data.groupby('ProductName').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum')
).reset_index().sort_values(by='total_quantity_sold', ascending=False)

# Plot for Top-selling Products by Quantity
plt.figure(figsize=(10, 6))
plt.bar(top_selling_by_quantity['ProductName'], top_selling_by_quantity['total_quantity_sold'])
plt.xticks(rotation=90)
plt.title('Top-selling Products by Quantity')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Sold')
plt.tight_layout()
plt.show()

conn.close()
