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
# Correlation Analysis between Product Attributes
correlation_data = product_sales_data[['Price', 'CPUFreq', 'Ram', 'Inches', 'QuantitySold']]
correlation_matrix = correlation_data.corr()

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
