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

sales_summary = product_sales_data.groupby('ProductName').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index()

price_summary = product_sales_data.groupby('ProductName').agg(
    average_price=pd.NamedAgg(column='Price', aggfunc='mean'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index()

product_sales_data['SaleDate'] = pd.to_datetime(product_sales_data['SaleDate'])
product_sales_data['Month'] = product_sales_data['SaleDate'].dt.to_period('M')

monthly_sales = product_sales_data.groupby('Month').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index()

top_product_by_revenue = sales_summary.sort_values(by='total_revenue', ascending=False).iloc[0]

average_sales_per_product = product_sales_data.groupby('ProductName').agg(
    avg_sales_quantity=pd.NamedAgg(column='QuantitySold', aggfunc='mean')
).reset_index()

plt.figure(figsize=(10, 6))
plt.bar(sales_summary['ProductName'], sales_summary['total_revenue'])
plt.xticks(rotation=90)
plt.title('Total Revenue by Product')
plt.xlabel('Product Name')
plt.ylabel('Total Revenue')
plt.tight_layout()
plt.show()

conn.close()
