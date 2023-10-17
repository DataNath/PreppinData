# Read in packages:
import pandas as pd 
import numpy as np

# Read in data:
tp = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Tx Path.csv")
td = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Tx Detail.csv")
ai = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Acc Info.csv")

# Rename field names in the Transaction Path table:
tp = tp.rename(columns={"Account_To": "Account To", "Account_From": "Account From"})

# Filter out cancelled transactions:
td = td.loc[td["Cancelled?"] == 'N']

# Split the data into outgoing and incoming transactions:
out = pd.merge(tp, td, on="Transaction ID", how="inner")
out = out.drop(columns=["Transaction ID","Account To","Cancelled?"])
out = out.rename(columns={"Account From":"Account Number", "Transaction Date": "Balance Date"})
out["Value"] = out["Value"]*-1

inb = pd.merge(tp, td, on="Transaction ID", how="inner")
inb = inb.drop(columns=["Transaction ID", "Account From", "Cancelled?"])
inb = inb.rename(columns={"Account To": "Account Number", "Transaction Date": "Balance Date"})

# Bring the data together with the balance as of 31st Jan:
bal = ai.drop(columns=["Account Type","Account Holder ID"])
union = [bal, inb, out]
cb = pd.concat(union)

# Work out the order that transactions occur in for each account:
cb = cb.sort_values(by=["Account Number","Balance Date","Value"], ascending=[True, True, False], na_position='first')
cb = cb.reset_index()

# Use a running sum to calculate the balance for each account on each day:
cb1 = cb.groupby("Account Number", as_index=False).ffill()
cb1["ValueRS"] = cb.groupby("Account Number")["Value"].cumsum()
cb1 = cb1.reset_index()
cb1["Balance"] = cb1["Balance"] + np.where(pd.isnull(cb1["ValueRS"]), 0, cb1["ValueRS"])

# Tidy up old/temp columns and create a new dataframe for output:
output = pd.merge(cb, cb1, left_index=True, right_index=True)
output = output.drop(columns=["index_x","Balance Date_x","Balance_x","Value_x","level_0","index_y","ValueRS"])
output = output.rename(columns={"Balance Date_y": "Balance Date", "Balance_y": "Balance", "Value_y": "Transaction Value"})

# Output new dataframe as CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W9 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
