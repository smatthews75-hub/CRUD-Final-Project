import definitions as df_
file_path = './6000_Largest_Companies_ranked_by_Market_Cap.csv'
# groupables are defined as the strings of the field_types in the header of the csv file
# fields in the groupables are to be main groups of fields with names
GROUPABLES = ["Country"]
# we only give an option to rank one field
RANKED_FIELD = "Marketcap"
# where to store the ranking
STORED_RANKS = "Rank"
main_data_dict = {}
groups_of_data = {}

# main to make it clear and explicit !
if __name__ == '__main__':
    main_data_dict, groups_of_data = df_.read_n_dict(file_path, GROUPABLES, RANKED_FIELD, STORED_RANKS)

    
    # for name in main_data_dict:
    #     print(f"{name} : {main_data_dict[name]}")

    # for major_group in groups_of_data:
    #     print(f"<<< {major_group} >>>")
    #     for group_name in groups_of_data[major_group]:
    #         print(f"{group_name} === {groups_of_data[major_group][group_name]}")
