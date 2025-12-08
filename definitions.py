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
        answers_buffer = {} #' '
        # prompt the new key first '':false 'APPLE':true
        new_key = input(f"====================================== Create the {MAIN_KEY} : ").upper()
        if new_key == '': continue # make sure they dont create an empty named thing

        # Check if data with that key already exists
        if new_key in main_dict:
            print(f"{new_key} already existed ! {main_dict[new_key]}")
            if input("Use UPDATE mode to change that.\nWant to create something new ? (y/n)") in 'Yy': continue # restart the create loop
            else : break # exit create mode
        
        # prompt the fields of that key
        for field in fieldnames: # SYMBOL,MARKETCAP,PRICE (USD),COUNTRY
            while True:
                if field == RANKED_FIELD : # if the user has to fill in the RANKED_FIELD must be numeric
                    answers_buffer[field] = cf_.get_numeric(f">>> {field} : ")
                else : # anything else
                    answers_buffer[field] = input(f">>> {field} : ").upper()
                # make sure the user didn't input nothing
                if answers_buffer[field]: break
        
        # show a preview of what was typed
        print(f"{new_key} : {answers_buffer}")
        # confirm and only create when user confirms
        if input("Are you sure you want to create this ? (y/n)") in "Yy" :
            # default ranking, this rank only gets defined at writing to file
            answers_buffer[RANK_STORAGE] = -1
            # CREATE TO MAIN DICTIONARY
            main_dict[new_key] = answers_buffer
            # ALSO GROUP INTO THE GROUP DICT
            group_dict = cf_.add_groups(GROUPABLES, new_key, answers_buffer, group_dict)
            
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
        found_something = False # to check if something was found
        match input("Enter Action : "):
            case '1': found_something = cf_.show_by_main_keys(main_dict, MAIN_KEY) # display values of one key
            case '2': found_something = cf_.show_by_groups(group_dict, MAIN_KEY, RANKED_FIELD) # show by groups
            case '3': break

        if found_something: # only if something was found
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

        # ask which key of the data to update ''
        selected_key = input(f": : : : : Enter the {MAIN_KEY} of the data you want to change : (enter nothing to exit) ").upper()

        # if there is no such key that was selected ---> NEGATIVE CASE
        if not selected_key or selected_key not in main_dict:
            print(f"No such {MAIN_KEY} of that '{selected_key}' exists.")
            break # -------------------------------------------------

        # clean this selected key group before updating
        group_dict = cf_.remove_group(GROUPABLES, selected_key, main_dict[selected_key], group_dict)

        # change more than one values in the same selected key
        while True:
            # if the selected key exists, display info on these
            print(f"!!! < {MAIN_KEY} : {selected_key} > : ")
            for key, value in main_dict[selected_key].items():
                print(f">>> {key} : {value}")
            
            # ask which data  to update
            which_to_change = input("= = = = = Enter which do you want to change : (enter nothing to cancel) ").upper()

            # in case the user wants to change the name which is more significant
            if which_to_change == MAIN_KEY: # MAIN_KEY technically not in main_dict[selected_key]
                print(f"YOU ARE ABOUT TO CHANGE THE '{MAIN_KEY}' !")
                new_main_key = input(f"What shall be the new {MAIN_KEY} : ").upper()

                if not new_main_key : # ---> NEGATIVE CASE
                    print("You can't input nothing")
                    continue
                # update group and main dicts
                main_dict[new_main_key] = main_dict[selected_key] # new named key
                main_dict.pop(selected_key) # remove the previously named key
                selected_key = new_main_key # update the selected_key to be the new name as well
            
            # if the chosen thing to change is not present ---> NEGATIVE CASE
            elif which_to_change not in main_dict[selected_key]:
                print(f"No such key of that '{which_to_change}' exists.")
                break # -------------------------------------------------
            
            # ask for change
            elif which_to_change == RANK_STORAGE: # the field that stores the rank is not changable
                print("You're not allowed to change this ...")
            elif which_to_change == RANKED_FIELD: # the ranked field requires specific case management
                main_dict[selected_key][which_to_change] = cf_.get_numeric(f"Enter new value for {which_to_change} : ")
            else: # string based changes
                while True:
                    new_value = input(f"Enter new value for {which_to_change} : ").upper()
                    if new_value :
                        main_dict[selected_key][which_to_change] = new_value
                        break
                    else : print("You can't input nothing")
            
        # update groups, clever use of the remove and add to update values
        group_dict = cf_.add_groups(GROUPABLES, selected_key, main_dict[selected_key], group_dict)
    return main_dict, group_dict


# ============================================================================================== DELETE
# the classic delete part of the CRUD --- BY DEARRYL 252410907
def delete(main_dict, group_dict, FIELDNAMES, MAIN_KEY, GROUPABLES, RANKED_FIELD, RANK_STORAGE):
    print("Welcome to <<< DELETE MODE >>>")
    # program loop
    while True:

        # ask for what to remove
        key2del = input(f"Enter the {MAIN_KEY} you want to delete: ").upper()
        
        # if key2del exists and the user confirmed they want to delete it
        if key2del not in main_dict : print(f"{key2del} not found in the CSV data")
        elif input(f"Are you sure to delete {key2del}? (y/n): ") in 'Yy':
            # Removing it from group_dict first 
            group_dict = cf_.remove_group(GROUPABLES, key2del, main_dict[key2del], group_dict)
            # finally remove from the main data dictionary
            main_dict.pop(key2del)
        
        # ask if the user wants to break out of this program loop
        if input("Delete another ? (y/n)") not in 'Yy': break
    return main_dict, group_dict

# ============================================================================================== 
# ============================================================================================== 
# ============================================================================================== 
 
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