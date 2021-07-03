import pandas as pd
import json
import numpy as np

COUNTRIES_UE = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden"
]

def import_data():
    return pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')

def get_ue_data(df):
    return df[df["location"].isin(COUNTRIES_UE)].reset_index()

def get_data_last_date(df):
    max_date = df["date"].max()
    return df[df["date"]==max_date].reset_index()

def get_people_vaccinated_per_hundred_lastdate(df):
    return round(df["people_vaccinated_per_hundred"].dropna().values[0], 1)

def get_people_fully_vaccinated_per_hundred_lastdate(df):
    try:
        return round(df["people_fully_vaccinated_per_hundred"].dropna().values[0], 1)
    except Exception as e:
        print(e)
        return 0

def get_speed_people_vaccinated_per_hundred_lastdate(df):
    df = df.sort_values(by="date").dropna()
    try:
        return round(df["people_vaccinated_per_hundred"].values[-1] - df["people_vaccinated_per_hundred"].values[-7], 1)
    except Exception as e:
        print("ERROR : the value can not be returned")
        print(e)
        return 0

def sort_values_dict(dict, sort_by="people_vaccinated_per_hundred"):
    countries = [country for country in dict]
    values = [dict[country][sort_by] for country in dict]
    index_sorted = np.argsort(-np.array(values))
    return list(np.array(countries)[index_sorted])

def get_dict_vaccination_per_ue_country(df):
    dict_people_vaccinated = {"data": {}}
    for country in COUNTRIES_UE:
        df_country = df[df["location"]==country]
        df_lastdate = get_data_last_date(df_country)
        people_vaccinated_per_hundred = get_people_vaccinated_per_hundred_lastdate(df_lastdate)
        people_fully_vaccinated_per_hundred = get_people_fully_vaccinated_per_hundred_lastdate(df_lastdate)
        speed_people_vaccinated_per_hundred = get_speed_people_vaccinated_per_hundred_lastdate(df_country)
        dict_people_vaccinated["data"][country] = {"people_vaccinated_per_hundred": people_vaccinated_per_hundred,
                                                    "speed_people_vaccinated_per_hundred": speed_people_vaccinated_per_hundred,
                                                   "people_fully_vaccinated_per_hundred": people_fully_vaccinated_per_hundred}
    dict_people_vaccinated["countries_sorted"] = sort_values_dict(dict_people_vaccinated["data"])
    dict_people_vaccinated["max_date"] = df.date.max()
    return dict_people_vaccinated

def export_dict_people_vaccinated(dict_people_vaccinated):
    with open("../data/output/vaccination_ue_ranking.json", "w") as file:
        file.write(json.dumps(dict_people_vaccinated))


