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
        new_key = input(f"====================================== Create the {MAIN_KEY} : ").upper()


        # Check if data with that key already exists
        if new_key in main_dict:
            print(f"{new_key} already existed ! {main_dict[new_key]}")
            if input("Use UPDATE mode to change that.\nWant to create something new ? (y/n)") in 'Yy': continue # restart the create loop
            else : break # exit create mode
        

        # prompt the fields of that key
        for field in fieldnames:
            if field == RANKED_FIELD : # if the user has to fill in the RANKED_FIELD must be numeric
                answers_buffer[field] = cf_.get_numeric(f">>> {field} : ")
            else : # anything else
                answers_buffer[field] = input(f">>> {field} : ").upper()
        
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
        if input(": : : Create another ? (y/n)") not in 'Yy': break
    return main_dict, group_dict


# ============================================================================================== READ
# the classic read part of the CRUD
def read__(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print(" _ _ _ _ _ Welcome to <<< .READ. MODE >>> _ _ _ _ _ ")
    print("!! Read data information by their Keys or Groups. !!")
    # read loop
    while True:
        print(f"====================================== SELECT WHICH TO READ :")
        print(f"1. By '{MAIN_KEY}' keys\n2. By Field Groups\n3. Cancel & Exit")
        found_something = False
        match input("Enter Action : "):
            case '1': found_something = show_by_main_keys(main_dict, MAIN_KEY) # if something is found offer to read or update it
            case '2': found_something = show_by_group_values(main_dict, group_dict, MAIN_KEY, RANKED_FIELD) # show by groups
            case '3': break

        if found_something:
            match input("Do you want to proceed to : 1. Update | 2. Delete  | 3. Read | Exit : "):
                case '1': # The use of return is to quit this read scope imidiately after end of update process
                    return update(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE)
                case '2': # The use of return is to quit this read scope imidiately after end of delete process
                    return delete(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE)
                case '3': continue # restart read loop
                case _ : break # break out of loop
        elif input(": : : Want to find something else ? (y/n) ") in 'Yy' : continue # restart read loop
        else: break # break out of loop
    return main_dict, group_dict


# ============================================================================================== UPDATE
# the classic update part of the CRUD
def update(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print("_ _ _Welcome to <<< UPDATE MODE >>>_ _ _")
    print("Perform changes to any data information.")
    # update loop
    while True:

        selected_key = input(f": : : : : Enter the {MAIN_KEY} of the data you want to change : (enter nothing to exit) ").upper()
        # if there is no such key that was selected
        if selected_key not in main_dict:
            print(f"No such {MAIN_KEY} of that '{selected_key}' exists.")
            break # -------------------------------------------------

        # change more than one values in the same selected key
        while True:
            # if the selected key exists, display info on these
            print(f"!!! < {MAIN_KEY} : {selected_key} > : ")
            for key, value in main_dict[selected_key].items():
                print(f">>> {key} : {value}")
            which_to_change = input("= = = = = Enter which do you want to change : (enter nothing to exit) ")
            if which_to_change == MAIN_KEY:
                print(f"YOU ARE ABOUT TO CHANGE THE {MAIN_KEY} !")
                new_main_key = input(f"What shall be the new {MAIN_KEY} : ").upper()
                main_dict[new_main_key] = main_dict[selected_key] # new named key
                main_dict.pop(selected_key) # remove the previously named key
            
            # if the chosen thing to change is not present
            if which_to_change not in main_dict[selected_key]:
                print(f"No such key of that '{which_to_change}' exists.")
                break # -------------------------------------------------
            
            # ask to change it into what
            if which_to_change == RANK_STORAGE:
                print("You're not allowed to change this ...")
            elif which_to_change == RANKED_FIELD:
                main_dict[selected_key][which_to_change] = cf_.get_numeric(f"Enter new value for {which_to_change} : ")
            else:
                main_dict[selected_key][which_to_change] = input(f"Enter new value for {which_to_change} : ").upper()

    return main_dict, group_dict


# ============================================================================================== DELETE
# the classic delete part of the CRUD --- BY DEARRYL 252410907
def delete(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print("Welcome to <<< DELETE MODE >>>")
    while True:
        key2del = input("Enter the company you want to delete: ").upper()
        # Finding and deleting it from main_dict and group_dict
        if key2del in main_dict and input(f"Are you sure to delete {key2del}? (y/n): ") in 'Yy':
            # Removing it from group_dict first 
            for group in GROUPABLES:
                group_name = main_dict[key2del][group]
                group_name = group_name.upper() if type(group_name) == str else group_name
                group_dict[group][group_name].remove(key2del)
                
                if not group_dict[group][group_name]: group_dict[group].pop(group_name)

            main_dict.pop(key2del)
        else: print(f"{key2del} not found in the CSV data")
        if input("Delete another ? (y/n)") not in 'Yy': break
    return main_dict, group_dict

# ============================================================================================== 
# ============================================================================================== 
# ============================================================================================== 
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
def show_by_group_values(main_dict, group_dict, MAIN_KEY, RANKED_FIELD):
    # display each field
    for i, fields in enumerate(group_dict):
        print(f"{str(i+1)+'.':<3} {fields}")
    
    # get the user to choose the field
    selected_field = input("SELECT from which field is the group you're looking for : ").upper()

    # if the user selected a non option ---> NEGATIVE CASE
    if selected_field not in group_dict:
        print(f"'{selected_field}' is not an option.")
        return False
    
    # if the user did select an option, display the whole thing
    for j, groups in enumerate(group_dict[selected_field]):
        print(f"{j+1}.{groups:<15} | ", end='')
        if (j+1) % 10 == 0 : print()

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
        print(f"{keys:<15} | ", end='')
        if (k+1) % 10 == 0 : print()

    # get the user to choose a key from this group
    selected_key = input(f"\nSELECT which {MAIN_KEY} are you looking for ? ").upper()

    # if the user selected a non option ---> NEGATIVE CASE
    if selected_key not in group_dict[selected_field][selected_group]:
        print(f"{selected_key} does not exist in this group.")
        return False
    
    # FINALLY FOUND A MATCH BY GROUP
    print(f"!!! < {selected_key} > :")
    for key in main_dict[selected_key]:
        print(f">>> {key} : {main_dict[selected_key][key]}")
    return True # found something of that key

    
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