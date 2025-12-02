import core_functionality as cf_

# ============================================================================================== CREATE
# the classic create part of the CRUD
def create(main_dict, group_dict, FIELDNAMES, main_key, groupables, ranked_field, rank_storage):
    print("Welcome to Create mode")
    print("Create new objects to store in the CSV file")
    print("Note that the user is responsible for fields created")
    fieldnames = FIELDNAMES.copy() # This is so it doesnt change the real fieldname header
    # remember the main_key field is turned into the key so get rid of the main_key
    fieldnames.remove(main_key)
    # the user doesnt get to set this ranking
    fieldnames.remove(rank_storage)

    # create loop
    while True:
        answers_buffer = {}
        # prompt the new key first
        new_key = input(f"Set the {main_key} : ")
        # prompt the fields of that key
        for field in fieldnames:
            print(f"{field} == {ranked_field}")
            if field == ranked_field : # if the user has to fill in the ranked_field must be numeric
                answers_buffer[field] = cf_.get_numeric(f">>> {field} : ")
            else : # anything else
                answers_buffer[field] = input(f">>> {field} : ")
        
        # show a preview of what was typed
        print(f"{new_key} : {answers_buffer}")
        # confirm and only create when user confirms
        if input("Are you sure you want to create this ? (y/n)") in "Yy" :
            # default ranking, this rank only gets defined at writing to file
            answers_buffer[rank_storage] = -1
            # CREATE TO MAIN DICTIONARY
            main_dict[new_key] = answers_buffer
            # ALSO GROUP INTO GROUPABLES
            for group in groupables: # populate the group_dict
                group_name = answers_buffer[group] # get the name of the current row's group
                if group_name not in group_dict[group]: # create the list if it havent existed yet
                    group_dict[group][group_name] = [new_key] # This creates the first list of names!
                else : group_dict[group][group_name].append(new_key) # just append otherwise
            print(f"Created {new_key} : {main_dict[new_key]}")
            
        # ask if the user wants to create another field
        if input("Create another ? (y/n)") not in 'Yy': break
    return main_dict, group_dict


# ============================================================================================== READ
# the classic read part of the CRUD
def read(main_dict, group_dict, fieldnames):
    return main_dict, group_dict


# ============================================================================================== UPDATE
# the classic update part of the CRUD
def update(main_dict, group_dict, fieldnames):
    return main_dict, group_dict


# ============================================================================================== DELETE
# the classic delete part of the CRUD
def delete(main_dict, group_dict, fieldnames):
    return main_dict, group_dict

# simply display the menus of what to do
def display_menu():
    print('''
SELECT THE NUMBER FOR THESE ACTIONS :
>>> 1. CREATE
>>> 2. READ__
>>> 3. UPDATE
>>> 4. DELETE
>>> 5. Exit__''')
    return