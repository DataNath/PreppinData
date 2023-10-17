# Import packages:
import pandas as pd
import numpy as np

# Read in data:
cl = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W11 2023 Customer Locations.csv")
br = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W11 2023 Branches.csv")

# Append the Branch information to the Customer information:
cl["Key"] = 1
br["Key"] = 1

cb = pd.merge(cl, br, on="Key").drop("Key", axis=1)

# Transform the latitude and longitude into radians:
cb["Branch Long Radians"] = cb["Branch Long"] / (180/np.pi)
cb["Branch Lat Radians"] = cb["Branch Lat"] / (180/np.pi)
cb["Address Long Radians"] = cb["Address Long"] / (180/np.pi)
cb["Address Lat Radians"] = cb["Address Lat"] / (180/np.pi)

# Calculate the distance in miles between each Customer and Branch:
cb["Distance"] = round(3963 * np.arccos((np.sin(cb["Address Lat Radians"]) * np.sin(cb["Branch Lat Radians"])) + np.cos(cb["Address Lat Radians"]) * np.cos(cb["Branch Lat Radians"]) * np.cos(cb["Branch Long Radians"] - cb["Address Long Radians"])),2)

# Find the closest Branch for each Customer:
md = cb.groupby("Customer", as_index=False)["Distance"].min()
mf = pd.merge(cb, md, on=["Customer", "Distance"])

# For each Branch, assign a Customer Priority rating based on distance:
mf["Customer Priority"] = mf.groupby("Branch")["Distance"].rank().astype(int)

# Tidy up old/temp columns and prepare an output dataframe:
output = mf.drop(columns=["Address Lat Radians","Address Long Radians","Branch Long Radians","Branch Lat Radians"])
output = output[["Branch","Branch Long","Branch Lat","Distance","Customer Priority","Customer","Address Long","Address Lat"]]
output = output.sort_values(by=["Branch","Customer Priority"], ascending=True)

# Output new dataframe to a CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W11 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
