import re
import lib

# CAN WE ADD OPTION TO EXIT PARTWAY THROUGH, OR WAY TOO FIX WHEN YOU'RE GIVEN SUMMARY WITHOUT RESTARTING

# allowed values/limits
options_process = {'s' : 'serial dilution', 'm' : 'MALDI', 'sm' : 'serial dilution and MALDI plate spot'}
slot_range = range(1,6+1)
volume_range = range(1,20+1)
maldi_range = range(1,96+1)
maldi_spot_volume = 1 # μL


# User inputs to define method
def input_func():
    while True:

        agreement, end_flg = None, None
        process, tipbox_location, wellplate_location, maldiplate_location, dilution_ranges_name, number_of_replicates_m, buffer_location, matrix_location = None, None, None, None, None, None, None, None

        print('---------------------------------------')
        # method identification; all values optional 
        method_name = input("Enter method name: ")
        user_name = input("Enter user name: ")
        date = input("Enter date: ")
        comment = input("Comments: ")
        print('---------------------------------------')

        # Select method
        while True:
            [print(key,':',value) for key, value in options_process.items()] # display process options (serial dilution, maldi, both)
            process = input("What would you like to do? ") # user selects process 
            if process in options_process: 
                break # exit loop if process selected in process options
            print('invalid response') # return to start of loop if process selected not in options 
        print('---------------------------------------')

        # Input object locations
        while True:
            try:
                tipbox_location = int(input("What slot is the tipbox in? ")) # enter slot number (integer value)
            except:
                print('invalid response not a valid slot') # return if non-integer value is entered; stops error 
            else:
                if tipbox_location in slot_range: 
                    break # exit loop if slot number in range
                print('invalid response  not a valid slot') # return to start of loop if slot number not in range
        print('---------------------------------------')

        while True:
            try:
                wellplate_location = int(input("What slot is the 96 well plate in? ")) # enter slot number (integer value)
            except:
                print('invalid response - not a valid slot') # stops error if non-integer value is entered
            else: 
                if (wellplate_location in slot_range) and (wellplate_location != tipbox_location): 
                    break # exit loop if slot number in range AND not already filled
                print('invalid response - not a valid slot') # return to start of loop if slot number not in range OR slot already filled
        print('---------------------------------------')

        # For Serial Dilution then MALDI Plate Spot
        if process == 'sm':
            while True:
                try:
                    maldiplate_location = int(input("What slot is the MALDI plate in? ")) # enter slot number (integer value)
                except:
                    print('invalid response - not a valid slot') # stops error if non-integer value is entered
                else:
                    if (maldiplate_location in slot_range) and (maldiplate_location != tipbox_location) and (maldiplate_location != wellplate_location):
                        break # exit loop if slot number in range AND not already filled
                    print('invalid response - not a valid slot') # return to start of loop if slot number not in range OR slot already filled
            print('---------------------------------------')

        # Input sample details for serial dilution (number, name, desired dilution ranges)
        if process == 's' or process == 'sm':
            while True:
                try:
                    number_of_samples_s = int(input("Number of samples: ")) # enter number of samples (integer)
                except:
                    print('invalid response') # stops error if non-integer value is entered
                else:
                    dilution_ranges_name = {} # create dictionary
                    for counter_s in range(number_of_samples_s):
                        dilution_name = input(f"Sample {counter_s+1} name: ") # enter sample name; can be letter or integer
                        while dilution_name in dilution_ranges_name: # confirm sample name is unique
                            print("All samples must have unique names.")
                            dilution_name = input(f"Enter diffrent sample {counter_s+1} name: ") # enter new sample name if not unique
                        range_temp = input(f"{dilution_name} - Sample Range (eg.A1-A6): ") # enter serial dilution range; single values not accepted
                        while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2])[-][A-H]([1-9]|1[0-2]))$|^([A-H]([1-9]|1[0-2]))$'),range_temp)): # confirm dilution range is valid
                            print("All samples must have valid range.")
                            range_temp = input(f"{dilution_name} - Sample Range (eg.A1-A6): ") # enter new dilution range if not valid
                        dilution_ranges_name[dilution_name] = tuple(range_temp.split('-'))
                    if dilution_ranges_name != [('',)]: # WHAT IS THIS?
                        break
                    print('invalid response')
            print('---------------------------------------')
            
            # unnecessary
            # while True:
            #     print("Valid volume range", volume_range[0], "-", volume_range[-1], "μL")
            #     dilution_volume = int(input("What is the transfer volume? "))
            #     if dilution_volume in volume_range:
            #         break
            # print('---------------------------------------')
        
        # Input sammple details for maldi spot FOLLOWING serial dilution
        if process == 'sm':
            # Sample Number
            while True:
                agreement_sm = input("Spot all serial dilution wells on MALDI plate? [y] yes [n] no: ") # confirm sample number
                if agreement_sm == 'y':
                    break # exit loop if all serial dilution samples are to be spotted on MALDI plate
                if agreement_sm == 'n': # specify range if subset of serial dilution samples are to be spotted on MALDI plate
                    print('Specify range to spot on MALDI plate')
                    sample_ranges_sm = {} # create dictionary of sample ranges
                    for counter_sm in dilution_ranges_name: # for each named dilution range input samples to spot on MALDI plate
                        range_temp = input(f'{counter_sm} - Sample Range (eg.A1-A6): ') #fix issue w putting single value in range
                        while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2])[-][A-H]([1-9]|1[0-2]))$|^([A-H]([1-9]|1[0-2]))$'),range_temp)): # confirm sample range is valid
                            print("All samples must have valid range.")
                            dilution_name = input(f"Enter diffrent sample {counter_sm+1} range: ") # enter new sample range if not valid
                        sample_ranges_sm[counter_sm] = tuple(range_temp.split('-')) # split tuple
                    if sample_ranges_sm != [('',)]: # add check for overlapping dilution ranges/ out of range
                        break
                print('invalid response')
            print('---------------------------------------')
            # Replicate Number
            while True:
                try:
                    number_of_replicates_m = int(input("Number of replicates for each sample: ")) # enter number of replicates (integer)
                except:
                    print('invalid response') # stops error if non-integer value is entered
                else:
                    break
            print('---------------------------------------')
            # Buffer Location
            while True:
                try:
                    buffer_location = input("What well is the buffer in? (ex. A6) ") # enter buffer location
                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),buffer_location)): # confirm location valid
                        buffer_location = input("invalid response - not a valid well ")
                except:
                    print('invalid response')
                else:
                    buffer_location = tuple(buffer_location.split('-')) # ???????
                    break
            print('---------------------------------------')
            # Matrix Location 
            while True:
                try:
                    matrix_location = input("What well is the matrix in? (ex. A6) ") # enter matrix location
                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),matrix_location)): # confirm location valid
                        matrix_location = input("invalid response - not a valid well ")
                except:
                    print('invalid response')
                else: #fix me pls
                    matrix_location = tuple(matrix_location.split('-'))
                    break
            print('---------------------------------------')

        # For MALDI Plate Spot
        if process == 'm':
            # MALDI plate location
            while True:
                try:
                    maldiplate_location = int(input("What slot is the MALDI plate in? ")) # enter MALDI plate location (integer)
                except:
                    print('invalid response - not a valid slot')
                else:
                    if (maldiplate_location in slot_range) and (maldiplate_location != tipbox_location) and (maldiplate_location != wellplate_location):
                        break # exit loop if location is in range and not already filled
                    print('invalid response - not a valid slot')
            print('---------------------------------------')
            
            # Sample number, location, replicates
                # Here it is assumed sample 1 is in well A1; subsequent samples move down A until A12 then move to B1 and continue as such
            while True:
                try:
                    number_of_samples_m = int(input("Number of samples: ")) # enter number of samples (integer)
                    number_of_replicates_m = int(input("Number of replicates for each sample: ")) # enter number of replicates (integer)
                except:
                    print('invalid response') # stops error if non-integer entered
                else:
                    if(number_of_samples_m*number_of_replicates_m) <= maldi_range[-1]: # if number of samples greater than plate capacity return error
                        break            
                    print('Sample count exceeds plate.')   
            print('---------------------------------------')
            
            # Buffer location
            while True:
                try:
                    buffer_location = input("What well is the buffer in? (ex. A6) ") # enter buffer location
                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),buffer_location)): # confirm location valid
                        buffer_location = input("invalid response - not a valid well ")
                except:
                    print('invalid response')
                else: # remove?
                    buffer_location = tuple(buffer_location.split('-'))
                    break
            print('---------------------------------------')
            while True:
                try:
                    matrix_location = input("What well is the matrix in? (ex. A6) ") # enter matrix location
                    while not bool(re.search(re.compile('^([A-H]([1-9]|1[0-2]))$'),matrix_location)): # confirm location valid
                        matrix_location = input("invalid response - not a valid well ")
                except:
                    print('invalid response')
                else: #fix me pls # remove?
                    matrix_location = tuple(matrix_location.split('-'))
                    break
            print('---------------------------------------')
            

        # Method Summary: all input values printed at end of setup
        print('Method Name:', method_name)
        print('User:', user_name)
        print('Date:', date)
        print('Comments:', comment)
        print('Process:', options_process[process])
        print('Tipbox Slot:', tipbox_location)
        print('96 Well Plate Slot:', wellplate_location)

        # serial dilution
        if process == 's':
            print('Dilution Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in dilution_ranges_name.items()]
            print('Transfer Volume (μL):', dilution_volume)  # Not working rn because in macro

        # maldi spot
        if process == 'm':
            print('MALDI Plate Slot:', maldiplate_location)
            print('Number of Samples:', number_of_samples_m)
            print('Number of Replicates:', number_of_replicates_m)
            print('Buffer Location:', buffer_location)
            print('Matrix Location:', matrix_location)
            print(f'Default Spot Volume {maldi_spot_volume}μL.')
            print('Note: Samples collected from default locations.') # default locations as previously described

        # combined method
        if process == 'sm':
            print('MALDI Plate Slot:', maldiplate_location)
            print('Dilution Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in dilution_ranges_name.items()]
            print('Transfer Volume (μL):', dilution_volume) # Not working rn because in macro
            if agreement_sm == 'y':
                print('Sample Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in dilution_ranges_name.items()]
            else:
                print('Sample Ranges:');[print('\t',key,':',value[0], '-', value[1]) for key, value in sample_ranges_sm.items()]
            print('Number of Replicates:', number_of_replicates_m)
            print(f'Default spot volume {maldi_spot_volume}μL.')
        print('---------------------------------------')

        # Method Confirmation
        while agreement != 'n':
            print('Ensure tip box is full.')
            agreement = input("Review method. Correct? [y] yes [n] no: ")
            if agreement == 'y': 
                end_flg = True
                break # If method correct, exit loop and start run
            elif agreement == 'n':
                print('restarting') 
                break # if method incorrect, return to start of input         
            else:
                print('invalid response')
        
        if end_flg == True:
            break
    
    # Start Run
    return process, tipbox_location, wellplate_location, maldiplate_location, dilution_ranges_name, number_of_replicates_m, buffer_location, matrix_location, number_of_samples_m