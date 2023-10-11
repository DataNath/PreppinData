# Import packages:
import pandas as pd
import numpy as np

# Read in data:
xlsx = pd.ExcelFile("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W4 2023 New Customers.xlsx")
sheets = xlsx.sheet_names
jan = pd.read_excel(xlsx, sheet_name="January")
jan["Month"] = '1'
feb = pd.read_excel(xlsx, sheet_name="February")
feb["Month"] = '2'
mar = pd.read_excel(xlsx, sheet_name="March")
mar["Month"] = '3'
apr = pd.read_excel(xlsx, sheet_name="April")
apr["Month"] = '4'
may = pd.read_excel(xlsx, sheet_name="May")
may["Month"] = '5'
jun = pd.read_excel(xlsx, sheet_name="June")
jun["Month"] = '6'
jul = pd.read_excel(xlsx, sheet_name="July")
jul["Month"] = '7'
aug = pd.read_excel(xlsx, sheet_name="August")
aug["Month"] = '8'
sep = pd.read_excel(xlsx, sheet_name="September")
sep["Month"] = '9'
oct = pd.read_excel(xlsx, sheet_name="October")
oct["Month"] = '10'
nov = pd.read_excel(xlsx, sheet_name="November")
nov["Month"] = '11'
dec = pd.read_excel(xlsx, sheet_name="December")
dec["Month"] = '12'

# Correct spelling errors in field names:
aug = aug.rename(columns={"Demographiic": "Demographic"})
oct = oct.rename(columns={"Demagraphic": "Demographic"})

# Union all 12 months of data together into a single dataframe:
dfs = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
cb = pd.concat(dfs)

# Create a Joining Date field:
cb["Joining Date"] = pd.to_datetime(cb["Joining Day"].astype(str)+'/'+cb["Month"]+'/'+'2023', dayfirst=True)

# Reshape our data so we have a field for each demographic:
tf = cb.pivot(columns="Demographic", index=["ID","Joining Date"], values="Value")
tf = tf.reset_index()

# Remove duplicates based on a customer's earliest join date:
dd = tf.groupby(["ID","Account Type","Date of Birth","Ethnicity"], as_index=False)["Joining Date"].min()

# Output resulting data frame to CSV:
dd.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W4 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
