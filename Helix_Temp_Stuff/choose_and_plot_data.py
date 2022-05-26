#!/usr/bin/python

import time
import pprint
import json
import types
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime, timedelta
import TVAC_time_constants as TVAC_times
from load_data_files import load_mainhsk_names, load_mapping, load_minigoose, load_NASA_TCs, load_SFC, load_SFC_lists, load_var_names
from plotter_HELIX import make_plot, time_mask
from pip import main

times, df = load_SFC(1)
Xadc_array, magnetflows_array, mainhsk_temps_array, DCT_temps_array, helium_levels_array = load_SFC_lists(times,df)
mainhsk_names = load_mainhsk_names(1)
#NASA_TCs,NASA_names = load_NASA_TCs(1)
#minigoose = load_minigoose(1)
#mapping_df = load_mapping(1)
#print(mapping_df.head())
TVAC_times.all_delta_times(1)
#var_temp_names = load_var_names(1)
#print(mapping_df.loc[mapping_df['Component Name']=="alicat",mapping_df['Component Name']])
# THESE ARE FOR  plotting example mainhsk things like payton does.
#x,y=time_mask(times, mainhsk_temps_array[:,15],'Coldest')
#make_plot(x,y,'Gas panel-Coldest')
# for the gas panel
#x,y=time_mask(times, mainhsk_temps_array[:,15],'Flip')
#make_plot(x,y,'Gas panel-Flip')
# for the South TOF top 
#x,y=time_mask(times, mainhsk_temps_array[:,7],'Coldest')
#make_plot(x,y,'Top TOF South-Coldest')
# for the Battery rail 
x,y=time_mask(times, mainhsk_temps_array[:,4],'Flip')
make_plot(x,y,'Battery Rail-Flip',[-10,-22.5])

# try another variable now
# for NASA TCs
#x,y=time_mask(times, mainhsk_temps_array[:,4],'Flip')
#make_plot(x,y,'Battery Rail-Flip',[-10,-22.5])

# for minigoose
#

# for generic variable in SFC data
#

# CHANGE PAYTONS CODE TO FIRST ELIMINATE THE DICT BY GETTING JUST THE TEMPS
'''
test_payton=df['payload.fChargeControlStat.fPVA'].values
temp_list=[]
for i in test_payton: temp_list.append(i)
test_payton_array=np.asarray(temp_list)
print(type(test_payton_array[:,0]))
print("here comes the variables")
for i in test_payton_array[0,:]:
      print(type(i))
print(test_payton_array[0,0]) # this gives me a dictionary
paytons_keys=list(test_payton_array[0,0].keys())
print(paytons_keys)
print(test_payton_array[0,0].get(paytons_keys[-1]))
'''
