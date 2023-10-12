# Import packages:
import pandas as pd
import numpy as np

# Read in data
tp = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Tx Path.csv")
td = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Tx Detail.csv")
ai = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Acc Info.csv")
ah = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W7 2023 Acc Holders.csv")

# Change naming convention in the Transaction Path table:
tp = tp.rename(columns={"Account_To": "Account To", "Account_From": "Account From"})

# Split joint accounts to a row each in the Account Information:
ai["Account Holder ID"] = ai["Account Holder ID"].str.split(",")
ai = ai.explode("Account Holder ID")

# Ensure there are no null Account Holder ID values in the Account Information table:
ai = ai.loc[pd.notnull(ai["Account Holder ID"])]

# Make sure phone numbers start with 07 in the Account Holders table:
ah["Contact Number"] = '0' + ah["Contact Number"].astype(str)

# Bring the tables together:
cb = pd.merge(tp, td, on="Transaction ID", how="inner")
cb = pd.merge(cb, ai, left_on="Account From", right_on="Account Number", how="inner")
cb["Account Holder ID"] = cb["Account Holder ID"].astype(int)
cb = pd.merge(cb, ah, on="Account Holder ID",how="inner")

# Filter out cancelled transactions:
cb = cb.loc[cb["Cancelled?"] == 'N']

# Filter to transactions greater than £1,000 in value:
cb = cb.loc[cb["Value"] > 1000]

# Filter out platinum accounts:
cb = cb.loc[cb["Account Type"] != 'Platinum']

# Clean up old fields and create new data frame:
output = cb.drop(columns=["Account From","Cancelled?","Account Holder ID"])

# Output new data frame to a csv:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W7 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
