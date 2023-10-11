# Import packages:
import pandas as pd
import numpy as np

# Read in data:
tx = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W1 2023 Transactions.csv")

# Create Bank field by splitting off letters from Transaction Code:
tx["Bank"] = tx["Transaction Code"].str.split('-').str[0]

# Assign text labels to the Online or In-Person field based on numeric code:
tx["Online or In-Person"] = np.where(tx["Online or In-Person"] == 1, 'Online', 'In-Person')

# Change the data to be the day of the week:
tx["Transaction Date"] = pd.to_datetime(tx["Transaction Date"], dayfirst=True)
tx["Transaction Date"] = tx["Transaction Date"].dt.day_name()

# Create first output - Total transaction value by Bank:
o1 = tx.groupby("Bank").agg(Value = ("Value", "sum"))

# Create second output - Total transaction value by Bank, Weekday & Transaction Type:
o2 = tx.groupby(["Bank","Online or In-Person","Transaction Date"]).agg(Value = ("Value", "sum"))

# Crate third output - Total transaction value by Bank & Customer Code:
o3 = tx.groupby(["Bank","Customer Code"]).agg(Value = ("Value", "sum"))

# Output all dataframes to an Excel file, each in a different sheet:
with pd.ExcelWriter("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2023 Solution.xlsx") as target:
    o1.to_excel(target, "By Bank")
    o2.to_excel(target, "By Bank + Weekday + Tx Type")
    o3.to_excel(target, "By Bank + Customer Code")
    
# Print a completion message:
print("Output completed!")
