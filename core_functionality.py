import csv

# READ THE FILE AND LOAD THE CONTENTS INTO THE PROGRAM'S DICTIONARY
def read_n_dict(file_path, groupables, ranked_field, stored_ranks):
    main_dict = {}
    group_dict = {}
    # good practice to use with when opening files to properly auto close the file after use !
    with open(file_path, 'r', newline='', encoding='utf-8') as file_:
        # This CRUD is very field name dependent so we need to use DictReader to abstract away unneccessary complexity
        reader = csv.DictReader(file_)

        # initialize the group_dict
        for fieldname in groupables: group_dict[fieldname] = {}
        
        # populate the main dictionary and group
        for row_ in reader:
            name = row_.pop("Name") # store names
            row_[ranked_field] = int(row_[ranked_field]) # convert these as numerical value
            row_[stored_ranks] = int(row_[stored_ranks]) # convert these as numerical value
            main_dict[name] = row_ # main contains all the fields as value of each Name as key

            for group in groupables: # populate the group_dict
                group_name = row_[group]
                if group_name not in group_dict[group]: # create the list if it havent existed yet
                    group_dict[group][group_name] = [name] # This creates a list of names !
                else : group_dict[group][group_name].append(name) # just append otherwise !
    # return the dicts
    return reader.fieldnames, main_dict, group_dict



# Write back to file from the dictionaries
def write_dicts(file_path, headers, main_dict, group_dict, ranked_field, stored_rank):
    # get the rank sorted out
    ranking = group_dict[ranked_field].keys().sort()
    
    with open(file_path, "w", newline='', encoding='utf-8') as file_:
        writer = csv.DictWriter(file_, fieldnames=headers)