import csv

# READ THE FILE AND LOAD THE CONTENTS INTO THE PROGRAM'S DICTIONARY
def read_n_dict(file_path, MAIN_KEY, groupables, RANKED_FIELD, RANK_STORAGE):
    main_dict = {}
    group_dict = {}
    # good practice to use with when opening files to properly auto close the file after use !
    with open(file_path, 'r', newline='', encoding='utf-8') as file_:
        # This CRUD is very field name dependent so we need to use DictReader to abstract away unneccessary complexity
        reader = csv.DictReader(file_)
        # append the ranked field to groupables to make ranking easy
        groupables.append(RANKED_FIELD) 
        # initialize the group_dict, for each field make an empty dict
        for fieldname in groupables: group_dict[fieldname] = {}
        
        # populate the main dictionary and group
        for row_ in reader:
            name = (row_.pop(MAIN_KEY)).upper() # the Name field becomes the keys
            try :
                row_[RANKED_FIELD] = float(row_[RANKED_FIELD]) # convert these as numerical value
                row_[RANK_STORAGE] = int(row_[RANK_STORAGE]) # convert these as numerical value
            except ValueError: continue # skip invalid data

            row_buffer = {}
            for key, value in row_.items(): # clean up string fields
                if type(key) == str:
                    key = key.upper()
                if type(value) == str:
                    value = value.upper()
                row_buffer[key] = value
            
            main_dict[name] = row_buffer # main contains all the fields as value of each Name as key

            group_dict = handle_groups(groupables, name, row_, group_dict)
            
        # return the dicts and fieldname, also indicate that the groupables were changed
        return reader.fieldnames, groupables, main_dict, group_dict


# handle inserting new groups into the group dict
def handle_groups(GROUPABLES, name_key, row_value, group_dict):
    # for each fieldnames to be group-ed
    for group in GROUPABLES: # populate the group_dict
        group_name = row_value[group] # get the name of the current row's group
        group_name = group_name.upper() if type(group_name) == str else group_name
        if group_name not in group_dict[group]: # create the list if it havent existed yet
            group_dict[group][group_name] = [name_key] # This creates the first list of names!
        else : group_dict[group][group_name].append(name_key) # just append otherwise
    return group_dict


# Write back to file from the dictionaries
def write_dicts(file_path, headers, MAIN_KEY, main_dict, group_dict, RANKED_FIELD, stored_rank):
    with open(file_path, "w", newline='', encoding='utf-8') as file_:
        # get the rank sorted out in decending order
        ranked_values = list(group_dict[RANKED_FIELD].keys())
        ranked_values.sort(reverse=True)

        # prepare the writer and write the header first
        writer = csv.DictWriter(file_, fieldnames=headers)
        writer.writeheader()

        # write to file based on the sorted ranks
        for rank, value in enumerate(ranked_values):
            # get the names first stored in group_dict
            list_of_names = group_dict[RANKED_FIELD][value]
            # if there are more than one name with the same ranked score 
            # then it is considered the same ranking
            for name in list_of_names:
                main_dict[name][stored_rank] = rank + 1 # set the rank first
                writer.writerow({MAIN_KEY : name, **main_dict[name]}) # WRITE !


# make it easy to prompt numerical values
def get_numeric(prompt_string):
    while True:
        try : return float(input(prompt_string))
        except ValueError : continue


# debug tools
def get_by_major_group(dict_, major_group):
    print(f"<<< {major_group} >>>")
    for target_ in dict_[major_group]:
        print(f"{target_:<20} === {dict_[major_group][target_]}")


def get_by_group(dict_, major_group, target_):
    print(f"{target_} === {dict_[major_group][target_]}")
