# Import packages
import pandas as pd
import numpy as np

# Read in data:
data = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\W1 2023.csv")

# Split the 'Store-Bike' field into 'Store' and 'Bike':
data[["Store", "Bike"]] = data["Store - Bike"].str.split(' - ', expand = True)

# Clean up the 'Bike' field to leave just three values (Mountain, Gravel, Road):
data["Bike"] = np.where(data["Bike"].str[0] == 'M','Mountain', np.where(data["Bike"].str[0] == 'R', 'Road', 'Gravel'))

# Create two different cuts of the date field - 'Quarter' and 'Day of Month':
data["Date"] = pd.to_datetime(data["Date"], dayfirst='True')
data["Quarter"] = data["Date"].dt.quarter
data["Day of Month"] = data["Date"].dt.day

# Remove first 10 orders as they were test values:
data = data.iloc[10:]

# Clean up old fields and create new data frame:
output = data.drop(columns = ["Store - Bike", "Date"])

# Output new data frame to CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
