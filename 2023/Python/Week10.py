# Import packages:
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Read in the data:
df = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W9 2023 Solution.csv")

# Create data scaffold of Jan 31st - Feb 14th:
start_date = datetime(2023, 1, 31)
end_date = datetime(2023, 2, 14)

date_range = [start_date + timedelta(days=x) for x in range ((end_date - start_date).days + 1)]

data = {
    'Balance Date': date_range
}

dr = pd.DataFrame(data)
dr["Key"] = 1

ac = pd.DataFrame()
ac["Account Number"] = df["Account Number"].unique()
ac["Key"] = 1

sc = pd.merge(ac, dr, on="Key").drop("Key",axis=1)

# Aggregate the data so we have a single balance for each account, each day:
ag = df.groupby(["Account Number","Balance Date"], as_index=False).agg({"Balance": 'sum', "Transaction Value": 'sum'})
ag["Balance Date"] = pd.to_datetime(ag["Balance Date"])

cb = pd.merge(sc, ag, how="left", on=["Account Number","Balance Date"])
cb["Balance"] = cb["Balance"].fillna(method='ffill')

# Create a parameter so a particular date can be selected:
selected_date = input("Please enter a date (using format YYYY-MM-DD): ")

# Filter to just this date:
cb = cb.loc[cb["Balance Date"] == selected_date]

# Create a new output data frame and output, making the date clear:
output = cb.groupby(["Account Number"], as_index=False).agg({"Balance": 'sum', "Transaction Value": 'sum'})
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W10 2023 Solution as of " + selected_date + ".csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
