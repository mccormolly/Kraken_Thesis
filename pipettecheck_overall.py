"""
Name: pipettecheck_overall.py

This script is used for mass-based validation of liquid handling.

Important: Edit macro on line 25 (currently draw_10ul_top) to change plunger rod displacement 
"""

# locations
slot2_middle = (164,40) # liquid draw location; middle of slot 2
weigh_dish = (214,40) # liquid dispense location; edge of slot 3

#EDIT MACRO USED FOR EACH RUN

from machine_interface import MachineConnection
with MachineConnection('/var/run/dsf/dcs.sock') as m:
   
    m.gcode("""M98 P"/macros/pickup_tip_A1" """) # pickup tip

    m.move(X = slot2_middle[0], Y = slot2_middle[1]) # go to middle of slot 2
    m.gcode("""M98 P"/macros/prime_tip" """) # prime tip

    for x in range(5): # repeat 5 times
        m.move(X = slot2_middle[0], Y = slot2_middle[1]) # go to middle of slot 2
        m.gcode("""M98 P"/macros/draw_10ul_top" """) # EDIT ME
        m.move(X = weigh_dish[0], Y = weigh_dish[1]) # go to weigh boat
        m.gcode("""M98 P"/macros/dispense_blowout" """) # dispense all liquid
    m.gcode("""M98 P"/macros/eject_tip" """) # after 5 replicates eject tip
    