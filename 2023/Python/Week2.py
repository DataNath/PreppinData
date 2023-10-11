# Import packages:
import pandas as pd
import numpy as np

# Read in data:
tx = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W2 2021 Transactions.csv")
sc = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W2 2021 Swift Codes.csv")

# Remove dashes from Sort Code field:
tx["Sort Code"] = tx["Sort Code"].str.replace('-','')

# Join datasets to bring in SWIFT code and Check Digits:
cb = pd.merge(tx, sc, on="Bank")

# Create IBAN field:
cb["IBAN"] = 'GB' + cb["Check Digits"] + cb["SWIFT code"] + cb["Sort Code"] + cb["Account Number"].astype(str)

# Clean up old fields and create new data frame:
output = cb.drop(columns=["Account Number","Sort Code","Bank","SWIFT code","Check Digits"])

# Output new data frame to CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W2 2021 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
