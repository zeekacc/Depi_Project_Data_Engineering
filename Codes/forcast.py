import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# Database connection parameters
server = 'DESKTOP-BIKQPHC'
database = 'LaptopDB'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

# Establish connection
conn = pyodbc.connect(conn_str)

# Query to get product sales data
query = """
SELECT 
    p.ProductID,  p.ProductName,  pd.CPUModel,  pd.CPUFreq,  pd.Ram,  pd.Inches, 
    pd.Price,f.SaleDate, f.QuantitySold, D f.TotalAmount
FROM 
    Product p
JOIN 
    ProductDetails pd ON p.ProductID = pd.ProductID
JOIN 
    FactSales f ON pd.DetailID = f.DetailID;
"""

# Fetch data
product_sales_data = pd.read_sql(query, conn)

# Data Preparation (Remove missing values, if any)
product_sales_data = product_sales_data.dropna()

# Feature selection (use product features to predict sales)
X = product_sales_data[['Price', 'CPUFreq', 'Ram', 'Inches']]
y = product_sales_data['QuantitySold']

# Check correlation matrix for multicollinearity
correlation_matrix = X.corr()
print("Correlation Matrix:")
print(correlation_matrix)

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Try using Random Forest Regressor for better performance
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print model evaluation metrics
print(f'Mean Squared Error (MSE): {mse}')
print(f'R-squared (R2) Score: {r2}')

# Cross-validation to check the model's generalization
cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='neg_mean_squared_error')
print(f'Cross-Validation MSE: {cv_scores.mean()}')

# Visualize predictions vs actual values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linewidth=2)  # line of perfect prediction
plt.title('Predicted vs Actual Sales Quantity')
plt.xlabel('Actual Quantity Sold')
plt.ylabel('Predicted Quantity Sold')
plt.show()

# Close the database connection
conn.close()
