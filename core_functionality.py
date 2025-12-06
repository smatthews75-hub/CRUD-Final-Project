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

            row_buffer = {} # buffer to transform everything to uppercase data
            for key, value in row_.items():
                if type(key) == str: key = key.upper()
                if type(value) == str: value = value.upper()
                row_buffer[key] = value # the buffer now stores normalized uppercase data
            
            main_dict[name] = row_buffer # main contains all the fields as value of each name as key

            group_dict = add_groups(groupables, name, row_, group_dict) # store names into groups
            
        # return the dicts and fieldname, also indicate that the groupables were changed
        return reader.fieldnames, groupables, main_dict, group_dict


# WRITE THE MAIN DATA DICTIONARY BACK TO THE FILE
def write_dicts(file_path, headers, MAIN_KEY, main_dict, group_dict, RANKED_FIELD, stored_rank):
    with open(file_path, "w", newline='', encoding='utf-8') as file_:
        # get the rank sorted out in decending order
        ranked_values = list(group_dict[RANKED_FIELD].keys()) # guaranteed sortable values
        ranked_values.sort(reverse=True)

        # prepare the writer and write the header first
        writer = csv.DictWriter(file_, fieldnames=headers)
        writer.writeheader() # self explanatory

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


# handle inserting new groups into the group dict
def add_groups(GROUPABLES, name_key, row_values, group_dict):
    # for each fieldnames to be group-ed
    for group in GROUPABLES: # populate the group_dict
        group_name = row_values[group] # get the name of the current row's group
        if type(group_name) == str : group_name = group_name.upper()
        if group_name not in group_dict[group]: # create the list if it havent existed yet
            group_dict[group][group_name] = [name_key] # This creates the first list of names!
        else : group_dict[group][group_name].append(name_key) # just append otherwise
    return group_dict


# handle deleting the groups of the deleted data
def remove_group(GROUPABLES, name_key, row_values, group_dict):
    for group in GROUPABLES:
        group_name = row_values[group]
        group_dict[group][group_name].remove(name_key)
        
        # delete empty group_names
        if not group_dict[group][group_name]: group_dict[group].pop(group_name)
    return group_dict


# help the read function to display main_dict details
def show_by_main_keys(main_dict, MAIN_KEY):
    main_key = input(f">>> Enter {MAIN_KEY} : ").upper()
    if main_key in main_dict : # check if it exists yet
        print(f"!!! < {main_key} > :")
        for key, value in main_dict[main_key].items():
            print(f">>> {key} : {value}")
        return True # found something of that key
    print(f"{main_key} doesn't exist...")
    return False # found nothing


# help the read function to display based on group_dict
def show_by_groups(group_dict, MAIN_KEY, RANKED_FIELD):
    # display each field
    for fields in group_dict:
        print(f"=> {fields}")
    
    # get the user to choose the field
    selected_field = input("SELECT from which field is the group you're looking for : ").upper()

    # if the user selected a non option ---> NEGATIVE CASE
    if selected_field not in group_dict:
        print(f"'{selected_field}' is not an option.")
        return False
    
    # if the user did select an option, display the whole thing
    for j, groups in enumerate(group_dict[selected_field]):
        print(f"{j+1:<3}.{groups:<20} | ", end='')
        if (j+1) % 5 == 0 : print()

    # get the user ti choose a group
    selected_group = input(f"\nSELECT from which group is the {MAIN_KEY} you're looking for ? ").upper()

    # CHECK IF THIS SELECTED GROUP IS FROM THE RANKED FIELD
    if selected_field == RANKED_FIELD:  # if the group is numeric try to convert
        print("Trying to convert to float...")
        try : selected_group = float(selected_group)
        except : 
            print(f"Groups of this {selected_group} has to be a float.")
            return False
        
    # if the user selected a non option  ---> NEGATIVE CASE
    if selected_group not in group_dict[selected_field]:
        print(f"'{selected_group}' does not exist.")
        return False
    
    # if the user did select a valid group, display keys
    print(f"{MAIN_KEY} under this {selected_group} group :")
    for k, keys in enumerate(group_dict[selected_field][selected_group]):
        print(f"{keys:<20} | ", end='')
        if (k+1) % 5 == 0 : print()
    print()
    return True # found something of that key