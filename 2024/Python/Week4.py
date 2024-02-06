# Import packages:
import pandas as pd
import numpy as np

# Read in data:
fc = pd.concat(
    pd.read_excel(
        "G:\My Drive\My Documents\Python\Preppin Data\Inputs\PD 2024 Wk 4 Input.xlsx",
        sheet_name=[0, 1, 2],
    )
).reset_index()

sp = pd.read_excel(
    "G:\My Drive\My Documents\Python\Preppin Data\Inputs\PD 2024 Wk 4 Input.xlsx",
    sheet_name="Seat Plan",
)

# Create a data field to show whether the seat was booked by someone with a Flow Card:
fc["Flow Card?"] = np.where(fc["level_0"] == 0, "Flow Card", "No Flow Card")
fc = fc.drop(columns={"level_0", "level_1"})

# Aggregate the Seat Bookings to count how many bookings there are for each seat, each row, each class, for (non)-FC holders:
agg = (
    fc.groupby(["Class", "Seat", "Row", "Flow Card?"])
    .count()
    .reset_index()
    .rename(columns={"CustomerID": "Count"})
)

# Join the Seating Plan, only returning the records for seats that haven't been booked:
ro = pd.merge(agg, sp, how="outer", indicator=True)
ro = ro.loc[ro["_merge"] == "right_only"].drop(
    columns={"_merge", "Flow Card?", "Count"}
)

# Output the data:
ro.to_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W4 2024 Solution.csv",
    index=False,
    mode="w",
)

# Print a completion message:
print("Output completed!")
