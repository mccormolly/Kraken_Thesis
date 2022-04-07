# Kraken layout and object locations


# slot locations
slot1_origin_xy = (8,-25) # absolute coordinate of top right corner of slot 1
slot_delta_xy = (100,151) # distance from top right corner of one slot to next (mm)

# tip box
tip_A1_xy = (10,13) # distance from tip A1 to top right corner of slot (mm)
tip_separation_xy = (9,9) # distance between tips (mm)
tip_arrangement_colrow = (8,12) # number of columns (x) and rows (y) in tip box

# 96 well plate
well_A1_xy = (10,12) # distance in mm from well A1 to top right corner of slot
well_separation_xy = (9,9) # distance in mm between wells
well_arrangement_colrow = (8,12) # number of columns (x) and rows (y) in well plate

# MALDI plate holder
plate1_spotA1_xy = (66,12.8) # distance from plate 1 spotA1 to top right corner of slot (mm)
plate2_spotA1_xy = (66.6,73.3) # distance from plate 2 spotA1 to top right corner of slot (mm)
spot_separation_xy = (49.5/11,13.25/3) # distance between spots on plate (mm)
spot_arrangement_colrow = (12,8) # number of columns (x) and rows (y) on MALDI plate

# liquid pickup parameters
wellplate_liquid_pickup_height_z = 137
wellplate_liquid_mix_height_z = 135
wellplate_liquid_dispense_height_z = 135
maldi_dispense_height_z = 140.5 

# move parameters
clearance_height_wellplate_z = 153 
clearance_height_tipbox_z = 196 # tipbox clearance hight after picking up tip
clearance_height_maldi_z = 146 
tip_length = 20 

# liquid handling parameters
pipette_max_volume = 20 # uL 