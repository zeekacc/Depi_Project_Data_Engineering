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

# Top Products by Units Sold and Revenue
top_products_by_revenue_and_quantity = product_sales_data.groupby('ProductName').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index().sort_values(by=['total_quantity_sold', 'total_revenue'], ascending=False)

# Monthly Trend of Products Sold
product_sales_data['SaleDate'] = pd.to_datetime(product_sales_data['SaleDate'])
product_sales_data['Month'] = product_sales_data['SaleDate'].dt.to_period('M')

monthly_sales_trend = product_sales_data.groupby('Month').agg(
    total_quantity_sold=pd.NamedAgg(column='QuantitySold', aggfunc='sum'),
    total_revenue=pd.NamedAgg(column='TotalAmount', aggfunc='sum')
).reset_index()

# Correlation Analysis between Product Attributes
correlation_data = product_sales_data[['Price', 'CPUFreq', 'Ram', 'Inches', 'QuantitySold']]
correlation_matrix = correlation_data.corr()

# Plotting Results

# Plot for Top-selling Products by Quantity
plt.figure(figsize=(10, 6))
plt.bar(top_selling_by_quantity['ProductName'], top_selling_by_quantity['total_quantity_sold'])
plt.xticks(rotation=90)
plt.title('Top-selling Products by Quantity')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Sold')
plt.tight_layout()
plt.show()

# Plot for Top Products by Units Sold and Revenue
plt.figure(figsize=(10, 6))
plt.bar(top_products_by_revenue_and_quantity['ProductName'], top_products_by_revenue_and_quantity['total_revenue'])
plt.xticks(rotation=90)
plt.title('Top Products by Revenue and Quantity')
plt.xlabel('Product Name')
plt.ylabel('Total Revenue')
plt.tight_layout()
plt.show()

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

# Plot Correlation Matrix
plt.figure(figsize=(8, 6))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='none')
plt.colorbar()
plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()

conn.close()
