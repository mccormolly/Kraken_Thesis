from config import *

"""this is used to check the 20 uL pipetting. 

Briefly, the method involves picking up a tip, going to a specified dye well and drawing 20uL, then dispensing into another well. 

"""

# Variables
tip_box_A1 = (18, -12)

well_dye = (127, -13) # slot 2, B1
well_smp_1 = (136,-13) # slot 2, C1
smp_number = 24


from machine_interface import MachineConnection
with MachineConnection('/var/run/dsf/dcs.sock') as m:
    m.gcode("T0") # pickup tool
    print("Tool picked up")
    m.move(Z = clearance_height_tipbox_z)     
    tips = 0 
    for sample in range(smp_number):
        # calculate tip pickup
        pick_tip_x = tip_box_A1[0] + ((tips // tip_arrangement_colrow[1]) * tip_separation_xy[0])
        pick_tip_y = tip_box_A1[1] + ((tips % tip_arrangement_colrow[1]) * tip_separation_xy[1])  
        print(pick_tip_x, pick_tip_y, "tip pickup")
        m.move(X = pick_tip_x, Y = pick_tip_y) # move above tip
        m.gcode("""M98 P"/macros/pickup_tip" """) # call the macro to pickup tip)
        print("tip pickup sucessful")
        m.move(X = well_dye[0], Y = well_dye[1]) # move to dye well
        m.move(Z = wellplate_liquid_pickup_height_z)
        m.gcode("""M98 P"/macros/prime_tip" """) # call the macro to prime tip
        print("tip primed")
        m.gcode("""M98 P"/macros/draw_20ul" """) # call the macro to draw liquid
        m.move(Z = clearance_height_wellplate_z)
        print("20ul collected from", well_dye[0], well_dye[1])
        # calculate dispense well
        smp_dispense_x = well_smp_1[0] + ((tips//tip_arrangement_colrow[1]) * well_separation_xy[0])
        smp_dispense_y = well_smp_1[1] + ((tips%tip_arrangement_colrow[1]) * well_separation_xy[1])
        tips += 1
        m.move(X = smp_dispense_x, Y = smp_dispense_y) # move to dispense well
        m.move(Z = wellplate_liquid_dispense_height_z)
        m.gcode("""M98 P"/macros/dispense_blowout" """) # call the macro to dispense liquid
        print("20ul dispensed on", smp_dispense_x, smp_dispense_y)
        m.move(Z = clearance_height_wellplate_z)
        m.gcode("""M98 P"/macros/eject_tip" """) # call the macro to eject tip
        print("tip ejected")
        m.move(Z = clearance_height_tipbox_z)
    m.gcode("T-1") # return tool to holder