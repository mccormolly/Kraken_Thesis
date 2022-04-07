from config import *
from input import *

# this calculates the absolute coordinates of the top right point (well/tip) of any work item
    # required imputs: item identity and slot location of item
def item_absolute_xy(slot1_origin_xy, slot_delta_xy, item_A1_xy, item_location): 
    if(item_location <= 3):
        x = slot1_origin_xy[0] + slot_delta_xy[0]*(item_location - 1) + item_A1_xy[0]
        y = slot1_origin_xy[1] + item_A1_xy[1]
        return (x,y)
    else:
        x = slot1_origin_xy[0] + slot_delta_xy[0]*(item_location - 4) + item_A1_xy[0]
        y = slot1_origin_xy[1] + slot_delta_xy[1] + item_A1_xy[1]
        return (x,y)

# this takes single values in typical labelling format (A1 - H12) and turns the letters into numbers the computer can use
    # this will work with both upper and lower case letters
def name_index_to_number_index_single(indicies_name_value):
    if ord(indicies_name_value[0][0]) >= 97:
        row_temp_x1 = ord(indicies_name_value[0][0]) - 97
    else:
        row_temp_x1 = ord(indicies_name_value[0][0]) - 65
    row_temp_y1 = int(indicies_name_value[0][1:]) - 1
    indicies_number_value = (row_temp_x1,row_temp_y1)
    return indicies_number_value

# this takes ranges in typical labelling format (A1 - H12) and turns the letters into numbers the computer can use
    # this will work with both upper and lower case letters
def name_index_to_number_index(indicies_name_value):
    indicies_number_value = []
    for name_range in indicies_name_value:
        if ord(indicies_name_value[name_range][0][0]) >= 97:
            row_temp_x1 = ord(indicies_name_value[name_range][0][0]) - 97
        else:
            row_temp_x1 = ord(indicies_name_value[name_range][0][0]) - 65
        if ord(indicies_name_value[name_range][1][0]) >= 97:
            row_temp_x2 = ord(indicies_name_value[name_range][1][0]) - 97
        else:
            row_temp_x2 = ord(indicies_name_value[name_range][1][0]) - 65
        row_temp_y1 = int(indicies_name_value[name_range][0][1:]) - 1
        row_temp_y2 = int(indicies_name_value[name_range][1][1:]) - 1
        indicies_number_value.append((row_temp_x1,row_temp_y1,row_temp_x2,row_temp_y2))
    return indicies_number_value

# calculate tip box clearance height; dependent on tipbox location
def clearance_height(tipbox_location, clearance_height_tipbox_z, tip_length):
    if tipbox_location > 3: 
        return clearance_height_tipbox_z + tip_length 
    else:
        return clearance_height_tipbox_z 

# serial dilution function
def dilution(tipbox_A1_absolute_location, wellplate_A1_absolute_location, well_limit_number, clearance_height_z, tip_counter_final):
    from machine_interface import MachineConnection
    with MachineConnection('/var/run/dsf/dcs.sock') as m:
        m.gcode("T0") # pick up tool
        print("Tool picked up")
        m.move(Z = clearance_height_tipbox_z) # move to tipbox clearance height    
        tip_counter = 0  
        # define range of wells to be used
        for well_range in well_limit_number: 
            for well_counter_x in range(well_range[0],well_range[2]+1):
                well_counter_range_y_lower = 0
                well_counter_range_y_upper = well_arrangement_colrow[1] - 1
                if well_counter_x == well_range[0]:
                    well_counter_range_y_lower = well_range[1]
                if well_counter_x == well_range[2]:
                    well_counter_range_y_upper = well_range[3] - 1
                for well_counter_y in range(well_counter_range_y_lower,well_counter_range_y_upper+1):
                    # calculate tip pickup location
                    tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//(tip_arrangement_colrow[1])) * tip_separation_xy[0] # floor division
                    tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%(tip_arrangement_colrow[1])) * tip_separation_xy[1] # tip pickup location (Y) = Top right tip location + ((remainder of tip counter/tip arrangment) * tip separation)
                    tip_counter += 1
                    print(tip_pickup_x, tip_pickup_y, "tip pickup")
                    m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above pipette tip
                    m.gcode("""M98 P"/macros/pickup_tip" """)  # call the macro to pick up tip
                    # calculate pickup well location
                    well_sample_pickup_x = wellplate_A1_absolute_location[0] + well_counter_x * well_separation_xy[0]
                    well_sample_pickup_y = wellplate_A1_absolute_location[1] + well_counter_y * well_separation_xy[1]
                    print(well_sample_pickup_x, well_sample_pickup_y, "draw from well")
                    m.move(X = well_sample_pickup_x , Y = well_sample_pickup_y) # move above well
                    m.move(Z = wellplate_liquid_pickup_height_z) # bed moves up, tip submerged
                    m.gcode("""M98 P"/macros/prime_tip" """) # call the marco to prime tip
                    m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
                    m.move(Z = clearance_height_wellplate_z) # bed moves down
                    # calculate dispense well
                    well_sample_dispense_x = well_sample_pickup_x 
                    well_sample_dispense_y = well_sample_pickup_y + well_separation_xy[1]
                    if well_sample_dispense_y > (wellplate_A1_absolute_location[1] + (tip_arrangement_colrow[1]-1)*tip_separation_xy[1]): # if liquid was drawn from the last well in a column, move to top of next column to dispense
                        well_sample_dispense_x = well_sample_pickup_x + well_separation_xy[0]
                        well_sample_dispense_y = wellplate_A1_absolute_location[1]
                    print(well_sample_dispense_x, well_sample_dispense_y, "dispense into well")
                    m.move(X = well_sample_dispense_x , Y = well_sample_dispense_y) # move above well
                    m.move(Z = wellplate_liquid_dispense_height_z) # bed moves up, tip submerged
                    m.gcode("""M98 P"/macros/mix_liquid" """) # call the macro to mix liquid
                    print("mixing done")
                    m.move(Z = clearance_height_z) # bed moves down to tipbox clearance height           
                    m.gcode("""M98 P"/macros/eject_tip" """)  # call the macro to throw out tip
                    print("tip ejected")
                    tip_counter_final = tip_counter # track of how many tips used
    return tip_counter_final

# MALDI spotting function
def maldi_spot(tipbox_A1_absolute_location, wellplate_A1_absolute_location, maldi_A1_absolute_location, well_limit_number, number_of_replicates_m, clearance_height_z, buffer_location_number, matrix_location_number, tip_counter_final):
    from machine_interface import MachineConnection
    with MachineConnection('/var/run/dsf/dcs.sock') as m:
        m.gcode("T0") # pick up tool
        print("Tool picked up")
        m.move(Z = clearance_height_tipbox_z) # bed moves down to tipbox clearance height  
        tip_counter = 0
        tip_counter_final = 0
        # For sample spot on MALDI plate
            # define range of wells to be used
        for well_range in well_limit_number:
            for well_counter_x in range(well_range[0],well_range[2]+1):
                well_counter_range_y_lower = 0
                well_counter_range_y_upper = well_arrangement_colrow[1] - 1 
                if well_counter_x == well_range[0]:
                    well_counter_range_y_lower = well_range[1]
                if well_counter_x == well_range[2]:
                    well_counter_range_y_upper = well_range[3] - 1
                for well_counter_y in range(well_counter_range_y_lower,well_counter_range_y_upper+1):
                    # calculate tip pickup location
                    tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//(tip_arrangement_colrow[1])) * tip_separation_xy[0]
                    tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%(tip_arrangement_colrow[1])) * tip_separation_xy[1]
                    print(tip_pickup_x, tip_pickup_y, "tip pickup")
                    m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above top                  
                    m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pick up tip
                    # calculate pickup well location
                    well_sample_pickup_x = wellplate_A1_absolute_location[0] + well_counter_x * well_separation_xy[0]
                    well_sample_pickup_y = wellplate_A1_absolute_location[1] + well_counter_y * well_separation_xy[1]
                    print(well_sample_pickup_x, well_sample_pickup_y, "draw from well")
                    m.move(X = well_sample_pickup_x , Y = well_sample_pickup_y) # move above well
                    m.move(Z = wellplate_liquid_pickup_height_z)
                    m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
                    m.gcode("""M98 P"/macros/draw_20ul" """) # CHANGE FEED RATE IN MACRO # call the macro to draw liquid
                    m.move(Z = clearance_height_wellplate_z)
                    # calculate dispense location
                    for replicate_count in range(0, number_of_replicates_m):
                        spot_dispense_x = maldi_A1_absolute_location[0] - (spot_separation_xy[0] * ((number_of_replicates_m * tip_counter + replicate_count) % spot_arrangement_colrow[0]))
                        spot_dispense_y = maldi_A1_absolute_location[1] + spot_separation_xy[1] * ((number_of_replicates_m * tip_counter + replicate_count) // spot_arrangement_colrow[0])
                        print(spot_dispense_x, spot_dispense_y, "dispense on spot")
                        m.move(X = spot_dispense_x, Y = spot_dispense_y) # move above spot
                        m.move(Z = maldi_dispense_height_z)                
                        m.gcode("""M98 P"/macros/relative_dispense_1ul" """) # call the macro to dispense liquid                    
                        m.move(Z = clearance_height_maldi_z)
                    m.move(Z = clearance_height_z)            
                    m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to throw out tip
                    print("tip ejected")
                    tip_counter += 1
                    tip_counter_final = tip_counter

        # For buffer spot on MALDI plate
        for maldi_spot_count in range(0, tip_counter_final * number_of_replicates_m): 
            if maldi_spot_count % number_of_replicates_m == 0:
                m.move(Z = clearance_height_z)            
                m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to throw out tip
                print("tip ejected")
                # calculate tip pickup location
                tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//tip_arrangement_colrow[1]) * tip_separation_xy[0]
                tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%tip_arrangement_colrow[1]) * tip_separation_xy[1]
                print(tip_pickup_x, tip_pickup_y, "tip pickup")
                m.move (Z = clearance_height_tipbox_z)
                m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above tip            
                m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pick up tip
                # calculate buffer location
                buffer_location_x = wellplate_A1_absolute_location[0] + well_separation_xy[0] * buffer_location_number[0]
                buffer_location_y = wellplate_A1_absolute_location[1] + well_separation_xy[1] * buffer_location_number[1]
                print(buffer_location_x, buffer_location_y, "buffer taken from well")
                m.move(X = buffer_location_x, Y = buffer_location_y) # move above buffer well
                m.move( Z = wellplate_liquid_pickup_height_z)
                m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
                print("tip primed")
                m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
                print("liquid draw")
                m.move(Z = clearance_height_wellplate_z)
                tip_counter += 1
                tip_counter_final = tip_counter
            # calculate dispense location on MALDI plate
            spot_dispense_x = maldi_A1_absolute_location[0] - (spot_separation_xy[0] * (maldi_spot_count % spot_arrangement_colrow[0])) 
            spot_dispense_y = maldi_A1_absolute_location[1] + spot_separation_xy[1] * (maldi_spot_count // spot_arrangement_colrow[0])
            print(spot_dispense_x, spot_dispense_y, "buffer added to spot")
            m.move(X = spot_dispense_x, Y = spot_dispense_y) # move above spot
            m.move(Z = maldi_dispense_height_z)
            m.gcode("""M98 P"/macros/relative_dispense_1ul" """) # call the macro to dispense liquid
            print("buffer dispensed")
            m.move(Z = clearance_height_maldi_z)


        # Accept matrix addition
            # this provides a pause in method for incubation and rinsing
        while True:
            continue_response = input("Would you like to proceed with adding matrix? [y] yes [n] no: ")
            if continue_response == 'y':
                break

        # For matrix spot on MALDI plate
        for maldi_spot_count in range(0, tip_counter_final * number_of_replicates_m):
            if maldi_spot_count % number_of_replicates_m == 0:
                m.move(Z = clearance_height_z)
                m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to throw out tip
                print("tip ejected")
                m.move(Z = clearance_height_tipbox_z)
                # calculate tip pickup location
                tip_pickup_x = tipbox_A1_absolute_location[0] + (tip_counter//tip_arrangement_colrow[1]) * tip_separation_xy[0]
                tip_pickup_y = tipbox_A1_absolute_location[1] + (tip_counter%tip_arrangement_colrow[1]) * tip_separation_xy[1]
                print(tip_pickup_x, tip_pickup_y, "tip pickup")
                m.move(X = tip_pickup_x, Y = tip_pickup_y) # move above tip
                m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pick up tip
                # calculate matrix location
                matrix_location_x = wellplate_A1_absolute_location[0] + well_separation_xy[0] * matrix_location_number[0]
                matrix_location_y = wellplate_A1_absolute_location[1] + well_separation_xy[1] * matrix_location_number[1]
                print(matrix_location_x, matrix_location_y, "matrix taken from well")
                m.move(X = matrix_location_x, Y = matrix_location_y) # move above matrix well
                m.move( Z = wellplate_liquid_pickup_height_z)
                m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
                print("tip primed")
                m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
                print("liquid draw")                               
                m.move(Z = clearance_height_wellplate_z)
                tip_counter += 1
                tip_counter_final = tip_counter
            # Calculate dispense location on MALDI plate
            spot_dispense_x = maldi_A1_absolute_location[0] - (spot_separation_xy[0] * (maldi_spot_count % spot_arrangement_colrow[0])) 
            spot_dispense_y = maldi_A1_absolute_location[1] + spot_separation_xy[1] * (maldi_spot_count // spot_arrangement_colrow[0])
            m.move(X = spot_dispense_x, Y = spot_dispense_y) # move above spot
            print(spot_dispense_x, spot_dispense_y, "matrix added to spot")
            m.move(Z = maldi_dispense_height_z)
            m.gcode("""M98 P"/macros/relative_dispense_1ul" """) # call the macro to dispense liquid
            print("matrix dispense")
            m.move(Z = clearance_height_maldi_z)
        m.move(Z = clearance_height_z)
        m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to eject tip
        print("tip ejected")
    return tip_counter_final