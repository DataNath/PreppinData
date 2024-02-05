# Import packages:
import pandas as pd
import numpy as np

# Read in data:
df1 = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2024 Solution - Flow Card.csv"
)
df2 = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2024 Solution - Non-Flow Card.csv"
)

# Union the two files together:
df = pd.concat([df1, df2])

# Convert the Date field to Quarter number instead:
df["Quarter"] = pd.to_datetime(df["Date"], dayfirst=True).dt.quarter

# Aggregate the data to median/min/max price per Quarter/Flow Card?/Class:
agg = df.groupby(["Quarter", "Flow Card?", "Class"], as_index=False).agg(
    Median=("Price", np.median), Min=("Price", np.min), Max=("Price", np.max)
)

# Create seperate flows where each has one of the aggregated measures:
med = agg.drop(columns=["Min", "Max"])
min = agg.drop(columns=["Median", "Max"])
max = agg.drop(columns=["Min", "Median"])

# Pivot the data to have a column per class for each quarter and whether the passenger had a flow card:
med = med.pivot(columns="Class", index=["Quarter", "Flow Card?"], values="Median")
min = min.pivot(columns="Class", index=["Quarter", "Flow Card?"], values="Min")
max = max.pivot(columns="Class", index=["Quarter", "Flow Card?"], values="Max")

# Optional: Add an extra column to label the measure used:
med["Measure"] = "Median"
min["Measure"] = "Minimum"
max["Measure"] = "Maximum"

# Union the flows back together:
cb = pd.concat([med, min, max])

# Change Economy > First, First Class > Economy, Business Class > Premium, Premium Economy > Business:
cb = cb.rename(
    columns={
        "Economy": "First",
        "First Class": "Economy",
        "Business Class": "Premium",
        "Premium Economy": "Business",
    }
).reset_index()

# Output the data:
cb.to_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W2 2024 Solution.csv",
    index=False,
    mode="w",
)

# Print a completion message:
print("Output completed!")
