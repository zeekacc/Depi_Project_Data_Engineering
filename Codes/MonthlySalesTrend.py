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

# Monthly Trend of Products Sold
product_sales_data['SaleDate'] = pd.to_datetime(product_sales_data['SaleDate'])
product_sales_data['Month'] = product_sales_data['SaleDate'].dt.to_period('M')

monthly_sales_trend = product_sales_data.groupby('Month').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index()

# Plot for Monthly Sales Trend
plt.figure(figsize=(10, 6))
plt.plot(monthly_sales_trend['Month'].astype(str), monthly_sales_trend['total_quantity_sold'], label='Quantity Sold')
plt.plot(monthly_sales_trend['Month'].astype(str), monthly_sales_trend['total_revenue'], label='Total Revenue')
plt.xticks(rotation=45)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.tight_layout()
plt.show()

conn.close()
