import core_functionality as cf_

# ============================================================================================== CREATE
# the classic create part of the CRUD
def create(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print(" _ _ _ _ _ Welcome to +++ CREATE MODE +++ _ _ _ _ _ ")
    print("!!! Create new data to be stored in the CSV file !!!")
    print("Note that the user is responsible for fields created")
    fieldnames = FIELDNAMES.copy() # This is so it doesnt change the real fieldname header
    # remember the MAIN_KEY field is turned into the key so get rid of the MAIN_KEY
    fieldnames.remove(MAIN_KEY)
    # the user doesnt get to set this ranking
    fieldnames.remove(RANK_STORAGE)

    # create loop
    while True:
        answers_buffer = {}
        # prompt the new key first
        new_key = input(f"Set the {MAIN_KEY} : ")
        # prompt the fields of that key
        for field in fieldnames:
            if field == RANKED_FIELD : # if the user has to fill in the RANKED_FIELD must be numeric
                answers_buffer[field] = cf_.get_numeric(f">>> {field} : ")
            else : # anything else
                answers_buffer[field] = input(f">>> {field} : ")
        
        # show a preview of what was typed
        print(f"{new_key} : {answers_buffer}")
        # confirm and only create when user confirms
        if input("Are you sure you want to create this ? (y/n)") in "Yy" :
            # default ranking, this rank only gets defined at writing to file
            answers_buffer[RANK_STORAGE] = -1
            # CREATE TO MAIN DICTIONARY
            main_dict[new_key] = answers_buffer
            # ALSO GROUP INTO GROUPABLES
            group_dict = cf_.handle_groups(GROUPABLES, new_key, answers_buffer, group_dict)
            
            print(f"Created {new_key} : {main_dict[new_key]}")
            
        # ask if the user wants to create another field
        if input("Create another ? (y/n)") not in 'Yy': break
    return main_dict, group_dict


# ============================================================================================== READ
# the classic read part of the CRUD
def read__(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print(" _ _ _ _ _ Welcome to <<< .READ. MODE >>> _ _ _ _ _ ")
    print("!! Read data information by their Keys or Groups. !!")
    # read loop
    while True:
        print("SELECT WHICH TO READ :")
        print("")
    return main_dict, group_dict


# ============================================================================================== UPDATE
# the classic update part of the CRUD
def update(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print("Welcome to <<< UPDATE MODE >>>")
    return main_dict, group_dict


# ============================================================================================== DELETE
# the classic delete part of the CRUD
def delete(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print("Welcome to <<< DELETE MODE >>>")
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