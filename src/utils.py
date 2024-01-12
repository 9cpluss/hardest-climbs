import pandas as pd


grades = pd.DataFrame(
    data=[
        [0, "9b", "5.15b", "sport"],
        [1, "9b/+", "5.15b/c", "sport"],
        [2, "9b+", "5.15c", "sport"],
        [3, "9b/c", "5.15c/d", "sport"],
        [4, "9c", "5.15d", "sport"],
        [5, "9c/+", "5.15d/16a", "sport"],
        [6, "9c+", "5.16a", "sport"],
        [0, "8C", "V15", "bouldering"],
        [1, "8C/+", "V15/V16", "bouldering"],
        [2, "8C+", "V16", "bouldering"],
        [3, "8C+/9A", "V16/V17", "bouldering"],
        [4, "9A", "V17", "bouldering"],
        [5, "9A/+", "V17/18", "bouldering"],
        [6, "9A+", "V18", "bouldering"],
    ],
    columns=["rank", "french", "us", "style"]
)


def json_to_dataframe(json_data: dict) -> pd.DataFrame:
    """
    Loads the JSON structure into a DataFrame for easier handling

    :param json_data: The raw JSON structure

    :return: A DataFrame with one row per ascent
    """
    data = pd.DataFrame.from_dict(data=json_data)

    data["climbers"] = data.apply(lambda row: row["repeat"] + [row["fa"]], axis=1)
    data = data.explode("climbers")

    data["is_fa"] = data["climbers"] == data["fa"]

    data["first_name"] = None
    data["last_name"] = None
    data[["first_name", "last_name"]]= data["climbers"].str.split(" ", n=1, expand=True)

    # data["video"] = data.apply(lambda row: row["videos"].get(row["last_name"]), axis=1)

    data["climber_key"] = data["first_name"].str.lower() + "+" + data["last_name"].str.lower()
    data["route_key"] = data["name"].str.replace(" ", "+").str.lower()

    data = data.merge(grades, left_on="grade", right_on="french")

    data = data.drop(columns=["grade"])

    return data
