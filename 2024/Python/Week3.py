# Import packages:
import pandas as pd
import numpy as np

# Read in targets:
tg = (
    pd.concat(
        pd.read_excel(
            "G:\My Drive\My Documents\Python\Preppin Data\Inputs\PD 2024 Wk 3 Input.xlsx",
            sheet_name=None,
        ),
        ignore_index=False,
    )
    .reset_index(level=0)
    .rename(columns={"level_0": "Quarter"})
)

# Input 2024 Week 1 outputs:
rs1 = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2024 Solution - Flow Card.csv"
)
rs2 = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W1 2024 Solution - Non-Flow Card.csv"
)

rs = pd.concat([rs1, rs2])

# Correct the Class column as per 2024 Week 2:
rs["NewClass"] = rs["Class"].replace(
    to_replace=["Economy", "First Class", "Business Class", "Premium Economy"],
    value=["First", "Economy", "Premium", "Business"],
)

tg["NewClass"] = tg["Class"].replace(
    to_replace=["E", "FC", "BC", "PE"], value=["FC", "E", "PE", "BC"]
)

# Find the first letter from each word in the CLass to help with joining targets:
rs["FirstLetter"] = rs["NewClass"].str[:1]

# Change the date to a month number:
rs["MonthNumber"] = pd.to_datetime(rs["Date"], yearfirst=True).dt.month

# Total up the sales at the level of Class & Month:
agg = rs.groupby(["FirstLetter", "MonthNumber"], as_index=False)["Price"].sum()

# Join Targets data to the Sales data:
tg["FirstLetter"] = tg["NewClass"].str[:1]

cb = pd.merge(
    agg, tg, left_on=["MonthNumber", "FirstLetter"], right_on=["Month", "FirstLetter"]
)

# Calculate the difference between Sales and Target values per Class & Month:
cb["Difference to Target"] = cb["Price"] - cb["Target"]

# Reformat dataframe ready for output:
cb = cb.drop(columns={"FirstLetter", "Quarter", "Month"}).rename(
    columns={"MonthNumber": "Date"}
)

cb = cb[["Difference to Target", "Date", "Price", "Class", "Target"]]

# Output the data:
cb.to_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W3 2024 Solution.csv",
    index=False,
    mode="w",
)

# Print a completion message:
print("Output completed!")
