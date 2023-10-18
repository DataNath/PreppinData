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
    df["Month"] = df["Month"].str.extract(".+(\w{3}).csv")
    imported.append(df)

cb = pd.concat(imported, ignore_index=True)

# Create a Trade Order field showing the order of trades in each file, ordered by filename and id:
cb["Sector"] = np.where(pd.isnull(cb["Sector"]), "n/a", cb["Sector"])
cb["MonthAsDate"] = pd.to_datetime(cb["Month"], format="%b")
cb = cb.sort_values(by=["MonthAsDate", "id"])
cb["Trade Order"] = cb.groupby("Sector", as_index=False).cumcount() + 1

# Remove all data fields except Trade Order, Sector, Purchase Price:
cb = cb.drop(
    columns=[
        "id",
        "first_name",
        "last_name",
        "Ticker",
        "Market Cap",
        "Month",
        "MonthAsDate",
        "Market",
        "Stock Name",
    ]
)

# Create a Parameter to allow the user to select the rolling number of trades for the moving average:
no_of_trades = int(input("Please enter a number of rolling trades to view: "))

# Workout the rolling average Purchase Price for each Trade Order in each Sector:
cb["Purchase Price"] = (
    cb["Purchase Price"].str.replace("$", "", regex=False).astype(float)
)

cb["Rolling Avg. Purchase Price"] = round(
    (
        cb.groupby("Sector", as_index=False)["Purchase Price"]
        .apply(lambda x: x.rolling(window=no_of_trades, min_periods=1).mean())
        .reset_index(level=0, drop=True)
    ),
    2,
)

# Filter for the last 100 trades for each sector:
cb = cb.groupby("Sector", as_index=False).tail(100)

# Create the Previous Trades field to show the oldest trade (1) through to latest (100):
cb["Previous Trades"] = (
    cb.sort_values(by="Trade Order").groupby("Sector", as_index=False).cumcount() + 1
)

# Clean up old/temp fields ready for output:
output = cb.drop(columns="Purchase Price")

# Output to CSV:
output.to_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W13 2023 Solution.csv",
    index=False,
    mode="w",
)

# Print completion message:
print("Output completed!")
