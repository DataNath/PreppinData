# Import packages:
import pandas as pd
import numpy as np
import glob

# Read in data:
files = glob.glob("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W8 2023*.csv")
imported = []
df = pd.DataFrame()
for f in files:
    df = pd.read_csv(f)
    df["Month"] = f
    df["Month"] = df["Month"].str.extract('.+(\w{3}).csv')
    imported.append(df)

cb = pd.concat(imported, ignore_index=True)

# Create a File Date field using the month from filename:
cb["File Date"] = pd.to_datetime(cb["Month"]+'2023',format='%b%Y')

# Clean the Market Cap value to remove any null rows:
cb = cb.loc[pd.notnull(cb["Market Cap"])]

# Categorise Purchase Price into groupings:
cb["Purchase Price"] = cb["Purchase Price"].str.replace("$","",regex=False).astype(float)
cb.loc[cb["Purchase Price"].between(0,24999.99),"PPC"]='Small'
cb.loc[cb["Purchase Price"].between(25000,49999.99),"PPC"]='Medium'
cb.loc[cb["Purchase Price"].between(50000,74999.99),"PPC"]='Large'
cb.loc[cb["Purchase Price"].between(75000,100000),"PPC"]='Very Large'

# Categorise Market Cap into groupings:
cb.loc[cb["Market Cap"].str.endswith('B'),"MC Numeric"]=(cb["Market Cap"].replace("[^\d.]","",regex=True).astype(float))*1000000000
cb.loc[cb["Market Cap"].str.endswith('M'),"MC Numeric"]=(cb["Market Cap"].replace("[^\d.]","",regex=True).astype(float))*1000000
cb.loc[~cb["Market Cap"].str.contains('[BM]',regex=True),"MC Numeric"]=(cb["Market Cap"].replace("[^\d.]","",regex=True).astype(float))

cb.loc[cb["MC Numeric"]<100000000,"MCC"]='Small'
cb.loc[cb["MC Numeric"].between(100000000,999999999),"MCC"]='Medium'
cb.loc[cb["MC Numeric"].between(1000000000,99999999999),"MCC"]='Large'
cb.loc[cb["MC Numeric"]>100000000000,"MCC"]='Huge'

# Rank the 5 highest purchases per file date, PPC and MCC:
cb["Rank"] = cb.groupby(["File Date","PPC","MCC"])["Purchase Price"].rank('max', ascending=False)

# Isolate records with a rank of 1 to 5:
cb = cb.loc[cb["Rank"] < 6]

# Clean up old fields and create new data frame:
output = cb.drop(columns=["id","first_name","last_name","Market Cap","Month"])
output = output.rename(columns={"MCC":"Market Capitalisation Category", "PPC":"Purchase Price Category", "MC Numeric":"Market Capitalisation"})
output = output[["Market Capitalisation Category","Purchase Price Category","File Date","Ticker","Sector","Market","Stock Name","Market Capitalisation","Purchase Price","Rank"]]

# Output new data frame to CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W8 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
