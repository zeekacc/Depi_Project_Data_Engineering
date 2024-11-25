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
# Top Products by Units Sold and Revenue
top_products_by_revenue_and_quantity = product_sales_data.groupby('ProductName').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index().sort_values(by=['total_quantity_sold', 'total_revenue'], ascending=False)
# Plot for Top Products by Units Sold and Revenue
plt.figure(figsize=(10, 6))
plt.bar(top_products_by_revenue_and_quantity['ProductName'], top_products_by_revenue_and_quantity['total_revenue'])
plt.xticks(rotation=90)
plt.title('Top Products by Revenue and Quantity')
plt.xlabel('Product Name')
plt.ylabel('Total Revenue')
plt.tight_layout()
plt.show()
conn.close()
