from config import *
from input import *
from lib import *

def main():
    tipbox_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, tip_A1_xy, tipbox_location)
    wellplate_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, well_A1_xy, wellplate_location)        
    clearance_height_z = clearance_height(tipbox_location, clearance_height_tipbox_z, tip_length)
    tip_counter_final_main = 0
    if process == 's':
        well_limit_number = name_index_to_number_index(dilution_ranges_name) # translate wells used into computer language
        tip_counter_final_main = dilution(tipbox_A1_absolute_location, wellplate_A1_absolute_location, well_limit_number, clearance_height_z, tip_counter_final_main)
    if process == 'm':
        well_limit_number = {(0,0,(number_of_replicates_m-1) // 12,(number_of_replicates_m-1) % 12)}
        maldi_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, plate1_spotA1_xy, maldiplate_location) #need to measure locations
        buffer_location_number = name_index_to_number_index_single(buffer_location)
        matrix_location_number = name_index_to_number_index_single(matrix_location)
        tip_counter_final_main = maldi_spot(tipbox_A1_absolute_location, wellplate_A1_absolute_location, maldi_A1_absolute_location, well_limit_number, number_of_replicates_m, clearance_height_z, buffer_location_number, matrix_location_number, tip_counter_final_main)
    if process == 'sm':
        well_limit_number = name_index_to_number_index(dilution_ranges_name) # translate wells used into computer language
        maldi_A1_absolute_location = item_absolute_xy(slot1_origin_xy, slot_delta_xy, plate1_spotA1_xy, maldiplate_location) #need to measure locations
        buffer_location_number = name_index_to_number_index_single(buffer_location)
        matrix_location_number = name_index_to_number_index_single(matrix_location)
        # check info
        tip_counter_final_main = dilution(tipbox_A1_absolute_location, wellplate_A1_absolute_location, well_limit_number, clearance_height_z, tip_counter_final_main)
        tip_counter_final_main = maldi_spot(tipbox_A1_absolute_location, wellplate_A1_absolute_location, maldi_A1_absolute_location, well_limit_number, number_of_replicates_m, clearance_height_z, buffer_location_number, matrix_location_number, tip_counter_final_main)
    from machine_interface import MachineConnection
    with MachineConnection('/var/run/dsf/dcs.sock') as m:
        m.gcode("T-1")


if __name__ == "__main__": # this needs fixed/more added
    process, tipbox_location, wellplate_location, maldiplate_location, dilution_ranges_name, number_of_replicates_m, buffer_location, matrix_location = input_func()
    main()
    print("Serial dilution complete on",*dilution_ranges_name.values())