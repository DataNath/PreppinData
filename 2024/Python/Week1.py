# Import packages:
import pandas as pd
import numpy as np

# Read in data:
df = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Inputs\PD 2024 Wk 1 Input.csv"
)

# Split Flight Details field:
fd = df["Flight Details"].str.split("//", expand=True)
tf = fd[2].str.split("-", expand=True).rename(columns={0: "From", 1: "To"})

# Merge the two dataframes and convert Price to a decimal:
mt = (
    pd.merge(fd, tf, how="inner", on=None, left_index=True, right_index=True)
    .drop(2, axis=1)
    .rename(columns={0: "Date", 1: "Flight Number", 3: "Class", 4: "Price"})
).astype({"Price": "float"})

# Convert Date to a date format (with a custom dd/mm/yyyy format):
mt["Date"] = pd.to_datetime(mt["Date"], yearfirst=True).dt.strftime("%d/%m/%Y")

# Merge with original dataframe to get remaining columns:
ft = pd.merge(mt, df, how="inner", on=None, left_index=True, right_index=True).drop(
    columns="Flight Details"
)

# Re-order dataframe fields:
ft = ft[
    [
        "Date",
        "Flight Number",
        "From",
        "To",
        "Class",
        "Price",
        "Flow Card?",
        "Bags Checked",
        "Meal Type",
    ]
]

# Change the Flow Card field to Yes/No values:
ft["Flow Card?"] = np.where(ft["Flow Card?"] == 1, "Yes", "No")

# Create two tables - one each for Flow Card holders and non-Flow Card holders:
ft1 = ft.loc[ft["Flow Card?"] == "Yes"]
ft2 = ft.loc[ft["Flow Card?"] == "No"]

# Output tables to CSVs:
ft1.to_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2024 Solution - Flow Card.csv",
    index=False,
    mode="w",
)
ft2.to_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2024 Solution - Non-Flow Card.csv",
    index=False,
    mode="w",
)

# Print a completion message:
print("Output completed!")
