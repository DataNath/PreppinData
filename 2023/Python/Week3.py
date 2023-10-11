# Import packages:
import pandas as pd
import numpy as np

# Read in data:
tx = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W3 2023 Transactions.csv")
tg = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W3 2023 Targets.csv")

# Filter transactions to only look at DSB data:
tx = tx.loc[tx["Transaction Code"].str.startswith("DSB")]

# Assign text values to Online or In-Person codes:
tx["Online or In-Person"] = np.where(tx["Online or In-Person"] == 1, 'Online', 'In-Person')

# Change the date to be a quarter
tx["Transaction Date"] = pd.to_datetime(tx["Transaction Date"], dayfirst=True)
tx["Quarter"] = tx["Transaction Date"].dt.quarter

# Aggregate to get sum of Value by Quarter & Type:
agg = tx.groupby(["Online or In-Person","Quarter"])["Value"].sum()

# Pivot quarterly targets to get a row for each Quarter & Type:
pv = pd.melt(tg, id_vars="Online or In-Person", var_name="Quarter", value_name="Quarterly Targets")

# Remove the Q from the Quarter field and make the dtype numeric:
pv["Quarter"] = pv["Quarter"].str.replace('Q','').astype(int)

# Join the two datasets together:
cb = pd.merge(agg, pv, on=["Online or In-Person","Quarter"])

# Calculate the variance to target for each row:
cb["Variance to Target"] = cb["Value"] - cb["Quarterly Targets"]

# Output resulting data frame to CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W3 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
