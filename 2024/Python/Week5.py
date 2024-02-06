# Import packages:
import pandas as pd
import numpy as np

# Read in data:
fl = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Inputs\Prep Air 2024 Flights.csv"
)

cs = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Inputs\Prep Air Customers.csv"
)

ts = pd.read_csv(
    "G:\My Drive\My Documents\Python\Preppin Data\Inputs\Prep Air Ticket Sales.csv"
)

# Create a dataset that gives customer details for flights booked in 2024 - include flight origin/destination:
bf = pd.merge(fl, ts, how="inner", on=["Flight Number", "Date"]).merge(
    cs, how="inner", on="Customer ID"
)

bf = bf[
    [
        "Date",
        "From",
        "To",
        "Flight Number",
        "Customer ID",
        "Last Date Flown",
        "first_name",
        "last_name",
        "email",
        "gender",
        "Ticket Price",
    ]
]

# Create a dataset that allows Prep Air to identify which flights haven't been booked yet in 2024 - add a timestamp for today:
nb = pd.merge(fl, ts, how="left", on=["Flight Number", "Date"], indicator=True)

nb = nb.loc[nb["_merge"] == "left_only"].drop(
    columns={"_merge", "Customer ID", "Ticket Price"}
)

nb["Flights unbooked as of"] = pd.Timestamp.today().strftime("%d/%m/%Y")

nb = nb[["Flights unbooked as of", "Date", "Flight Number", "From", "To"]]

# Create a dataset that shows which customers have yet to book a flight with Prep Air in 2024
# Create a field which allows Prep Air to see how many days it has been since their last flight (compare to 31/01/2024)
# Within last 3 months = Recent fliers, 3-6mo = Taking a break, 6-9mo = Been away a while, 9+mo = Lapsed

ub = pd.merge(ts, fl, how="inner", on=["Date", "Flight Number"]).merge(
    cs, how="right", on="Customer ID", indicator=True
)

ub = ub.loc[ub["_merge"] == "right_only"].drop(
    columns={"_merge", "Date", "Flight Number", "Ticket Price", "From", "To"}
)

ub["Days Since Last Flown"] = abs(
    (pd.to_datetime(ub["Last Date Flown"]) - pd.to_datetime("2024-01-31")).dt.days
)

ub["Months elapsed"] = abs(
    (
        (pd.to_datetime(ub["Last Date Flown"]) - pd.to_datetime("2024-01-31"))
        / pd.Timedelta(days=30.4375)
    ).astype(int)
)


def customer_category(months):
    if months <= 3:
        return "Recent fliers"
    elif 3 < months <= 6:
        return "Taking a break"
    elif 6 < months <= 9:
        return "Been away a while"
    else:
        return "Lapsed"


ub["Customer Category"] = ub["Months elapsed"].apply(customer_category)

ub = ub[
    [
        "Customer ID",
        "Customer Category",
        "Days Since Last Flown",
        "Last Date Flown",
        "first_name",
        "last_name",
        "email",
        "gender",
    ]
]

# Output the data:
with pd.ExcelWriter(
    "G:\My Drive\My Documents\Python\Preppin Data\Outputs\W5 2024 Solution.xlsx"
) as path:
    bf.to_excel(path, sheet_name="Booked Flights", index=False)
    nb.to_excel(path, sheet_name="Unbooked Flights", index=False)
    ub.to_excel(path, sheet_name="Unbooked Customers", index=False)

# Print output message:
print("Output completed!")
