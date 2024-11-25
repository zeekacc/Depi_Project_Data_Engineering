import pyodbc
import pandas as pd

# Database connection parameters
server = 'DESKTOP-BIKQPHC'  # Your SQL Server instance name
database = 'LaptopDB'  # Your database name

# Create a connection string for Windows Authentication
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

try:
    # Establish a connection to the database
    with pyodbc.connect(conn_str) as conn:
        print("Connection successful!")
        
        # Define the SQL query to join multiple tables and select specific fields
        query = """
        SELECT 
            PD.DetailID, PD.ProductID,P.ProductName,S.SupplierName,PD.CPUModel,
            PD.CPUFreq,PD.PrimaryStorage,PD.PrimaryStorageType,PD.SecondaryStorage,
            PD.SecondaryStorageType,PD.GPUCompany,PD.GPUModel,PD.OS,PD.Ram,PD.Screen,
            PD.Price,IL.QuantityInStock,IL.ReorderLevel,FS.SaleDate,FS.QuantitySold,
            FS.TotalAmount
        FROM 
            ProductDetails PD
        INNER JOIN 
            Product P ON PD.ProductID = P.ProductID
        INNER JOIN 
            Suppliers S ON P.SupplierID = S.SupplierID
        INNER JOIN 
            InventoryLevels IL ON PD.DetailID = IL.DetailID
        LEFT JOIN 
            FactSales FS ON PD.DetailID = FS.DetailID
        WHERE 
            FS.SaleDate >= '2024-01-01'  -- Example filter
        ORDER BY 
            FS.SaleDate DESC;  -- Order by sale date
        """
        
        # Use pandas to execute the query and load the data into a DataFrame
        product_details_data = pd.read_sql(query, conn)
        
        # Print the data
        print(product_details_data)

except pyodbc.Error as e:
    print("Error connecting to the database:", e)
