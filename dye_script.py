from config import *

# this is for checking the 1uL pipetting. I want it to pick up a tip, go to a specified well and pick up 20uL dye, then move to another specified well and dispense 1uL in x number of wells. 

# User Inputs
tip_box_A1 = (18, -12) #first tip to pick up
well_dye = (127, -13) # location of dye (slot 2, B1)
well_smp_1 = (163,-13) # location of sample 1 (slot 2, F1)
replicate_number = 4 # number of replicates for each draw
smp_number = 9 # total number of samples


from machine_interface import MachineConnection
with MachineConnection('/var/run/dsf/dcs.sock') as m:
    m.gcode("T0") # pick up tool
    print("Tool picked up")
    m.move(Z = clearance_height_tipbox_z)     
    tips = 0 
    for sample in range(smp_number):
        # calculate tip pickup location
        pick_tip_x = tip_box_A1[0] + ((tips // tip_arrangement_colrow[1]) * tip_separation_xy[0])
        pick_tip_y = tip_box_A1[1] + ((tips % tip_arrangement_colrow[1]) * tip_separation_xy[1])  
        print(pick_tip_x, pick_tip_y, "tip pickup")
        m.move(X = pick_tip_x, Y = pick_tip_y) # move above tip
        m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pickup tip
        print("tip pickup sucessful")
        # collect dye 
        m.move(X = well_dye[0], Y = well_dye[1]) 
        m.move(Z = wellplate_liquid_pickup_height_z)
        m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime time
        print("tip primed")
        m.gcode("""M98 P"/macros/draw_10ul_top" """) # call the macro to draw liquid
        m.move(Z = clearance_height_wellplate_z)
        print("10ul collected from", well_dye[0], well_dye[1])
        # go to first well in dispense series
        smp_dispense_x = well_smp_1[0] + ((tips//3) * well_separation_xy[0])
        smp_dispense_y = well_smp_1[1] + ((tips%3) * (well_separation_xy[1] * 4))
        tips += 1
        wells = 0
        # dispense 1 uL in each well
        for sample in range(replicate_number):
            smp_well_x = smp_dispense_x
            smp_well_y = smp_dispense_y + (well_separation_xy[1] * wells)
            m.move(X = smp_well_x, Y = smp_well_y)
            m.move(Z = wellplate_liquid_dispense_height_z)
            m.gcode("""M98 P"/macros/relative_dispense_1ul" """)
            print("1ul dispensed on", smp_well_x, smp_well_y)
            m.move(Z = clearance_height_wellplate_z)
            wells += 1
        m.gcode("""M98 P"/macros/eject_tip" """)
        print("tip ejected")
        m.move(Z = clearance_height_tipbox_z)
    m.gcode("T-1")