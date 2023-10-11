# Import packages
import pandas as pd
import numpy as np

# Read in data:
sd = pd.read_csv("G:\My Drive\My Documents\Python\Preppin Data\Inputs\W6 2023 Survey data.csv")

# Reshape data so that we have 5 rows for each customer:
mb = pd.melt(sd, id_vars="Customer ID", value_vars = ["Mobile App - Ease of Use","Mobile App - Ease of Access","Mobile App - Navigation","Mobile App - Likelihood to Recommend","Mobile App - Overall Rating"], var_name="Aspect", value_name="M_Score")
ol = pd.melt(sd, id_vars="Customer ID", value_vars = ["Online Interface - Ease of Use","Online Interface - Ease of Access","Online Interface - Navigation","Online Interface - Likelihood to Recommend","Online Interface - Overall Rating"], var_name="Aspect", value_name="O_Score")

# Clean the question categories so the platform is removed:
mb["Aspect"] = mb["Aspect"].str.split(' - ').str[1]
ol["Aspect"] = ol["Aspect"].str.split(' - ').str[1]

# Place mobile and online scores in separate fields on the same row:
cb = mb.merge(ol, on=["Customer ID", "Aspect"], how="inner")

# Exclude the Overall Ratings:
cb = cb.loc[cb["Aspect"] != 'Overall Rating']

# Calculate the average ratings for each platform for each customer:
ar = cb.groupby("Customer ID").agg(Avg_M_score=("M_Score","mean"), Avg_O_Score=("O_Score","mean"))
ar = ar.reset_index()

# Calculate the difference in average ratings between mobile and online for each customer:
ar["Difference in Averages"] = ar["Avg_M_score"]-ar["Avg_O_Score"]

# Categorise customers based on difference scores:
def pref_calc(row):
    if row["Difference in Averages"] >= 2:
        return 'Mobile App Superfan'
    elif row["Difference in Averages"] >= 1:
        return 'Mobile App Fan'
    elif row["Difference in Averages"] <= -2:
        return 'Online Interface Superfan'
    elif row["Difference in Averages"] <= -1:
        return 'Online Interface Fan'
    else:
        return 'Neutral'
    
ar["Preference"] = ar.apply(pref_calc, axis=1)

# Calculate the % of total customers in each category, rounded to 1 dp:
po = ar.groupby("Preference").agg(Pct_of_total=("Preference", "count"))
po["% of Total"] = round(po["Pct_of_total"]/len(ar)*100,1)

# Clean up old fields and create new data frame:
output = po.drop(columns="Pct_of_total")

# Output new data frame to CSV:
output.to_csv("G:\My Drive\My Documents\Python\Preppin Data\Outputs\W6 2023 Solution.csv", index=False, mode='w')

# Print a completion message:
print("Output completed!")
