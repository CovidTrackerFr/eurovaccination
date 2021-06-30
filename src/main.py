import vaccination_ue_ranking as ue
import prettyjson as pj

if __name__ == "__main__":
    df = ue.import_data()
    df_ue = ue.get_ue_data(df)
    dict_people_vaccinated = ue.get_dict_vaccination_per_ue_country(df_ue)
    ue.export_dict_people_vaccinated(dict_people_vaccinated)
    pj.pretty_all_json_files("./data/")