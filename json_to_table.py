from datetime import datetime
import json
import pandas as pd
import sqlalchemy
import itertools


data = pd.read_json("data/lead.json", encoding="utf-8")

climbers = set(data["fa"]) | set(itertools.chain.from_iterable(data.repeat))
climbs = set(data["name"])

# Climbs Table ----
climbs_table = pd.DataFrame({
    "ID": range(1, data.shape[0] + 1),
    "Name": data["name"],
    "Grade": data["grade"],
})

# Grades Table ----
grades_table = pd.DataFrame({
    "Grade": ["9c", "9b+", "9b/+", "9b"],
    "Rank": [1, 2, 3, 4],
})

# Climber Table ----
climber_table = pd.DataFrame({
    "ID": range(1, len(climbers) + 1),
    "FirstName": [c.split(" ")[0] for c in climbers],
    "LastName": [c.split(" ")[1] for c in climbers],
})

# First Ascent Table ----
fa_table = pd.DataFrame(columns=["ClimbID", "ClimberID", "Date"])
fa_table["ClimbID"] = climbs_table["ID"]
fa_table["Name"] = climbs_table["Name"]
for i, row in fa_table.iterrows():
    fa_name = data.loc[data["name"] == row["Name"], "fa"].values[0]
    date = data.loc[data["name"] == row["Name"], "date"].values[0]
    fa_id = climber_table.loc[climber_table["LastName"] == fa_name.split(" ")[1], "ID"].values[0]
    
    fa_table.loc[i, "ClimberID"] = fa_id
    fa_table.loc[i, "Date"] = date

fa_table = fa_table.drop(columns="Name")

# Repeat Table ----
repeat_table = pd.DataFrame(columns=["ClimbID", "ClimberID"])

for i, row in data[["name", "repeat"]].iterrows():
    climb_id = climbs_table.loc[climbs_table["Name"] == row["name"], "ID"].values[0]
    
    if len(row["repeat"]) > 0:
        for climber in row["repeat"]:
            name = climber.split(" ")[1]
            climber_id = climber_table.loc[climber_table["LastName"] == name, "ID"].values[0]
            repeat_table = repeat_table.append(
                other={
                    "ClimbID": climb_id,
                    "ClimberID": climber_id
                },
                ignore_index=True
            )


# A climb has one grade
# A climb has one FA
# A climb has one FA date
# A climb has Zero-to-Many repeats
# A climber has zero-to-many FA
# A climber has zero-to-many repeats

# ------------------------
# Tables
# ------------------------
# 
# Climbs
# ID | Name | Grade
#
# Climber
# ID | Name
# 
# First Ascents
# Climbs.ID | Climber.ID | Date
# 
# Repeats
# Climbs.ID | Climber.ID
#
# Videos
# Climbs.ID | Climber.ID | URL
