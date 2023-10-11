# Import packages:
import pandas as pd
import numpy as np

# Read in data:
tx = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W1 2023 Transactions.csv")

# Create Bank field by splitting off letters from Transaction Code:
tx["Bank"] = tx["Transaction Code"].str.split('-').str[0]

# Change Transaction Date to just be the month:
tx["Transaction Date"] = pd.to_datetime(tx["Transaction Date"], dayfirst=True)
tx["Transaction Date"] = tx["Transaction Date"].dt.month_name()

# Total up transactions so we have one row for each bank & month combination:
agg = tx.groupby(["Bank","Transaction Date"]).agg(Value = ("Value", "sum"))

# Rank each bank for their transaction value each month:
agg["Bank Rank per Month"] = agg.groupby("Transaction Date")["Value"].rank(method='average', ascending=False).astype(int)

# Find the average rank a bank has across all months:
ar = agg.groupby("Bank").agg(Avg_Rank_per_Bank = ("Bank Rank per Month", "mean"))

# Find the average transaction value per rank:
av = agg.groupby("Bank Rank per Month").agg(Avg_Transaction_Value_per_Rank = ("Value", "mean"))

# Without losing all other data fields, combine various aggregations with core data:
agg = agg.reset_index()
cb = (agg.merge(ar, on="Bank", how="inner")).merge(av, on="Bank Rank per Month", how="inner")

# Reorder fields and create new data frame:
output = cb[["Transaction Date","Bank","Value","Bank Rank per Month","Avg_Transaction_Value_per_Rank","Avg_Rank_per_Bank"]]

# Output new data frame to CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W5 2023 Solution.csv")

# Print a completion message:
print("Output completed!")
