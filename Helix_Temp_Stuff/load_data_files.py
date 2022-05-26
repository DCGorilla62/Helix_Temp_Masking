#!/usr/bin/python

import pprint
import json
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import csv
data_path=os.path.dirname(__file__)

def load_SFC(seq):
      print(os.getcwd())
      print(os.path.dirname(__file__))
      data_path=os.path.dirname(__file__)
      file_name="Plum_Brook_Feb7_1400hr_to_End.json"
      name_to_read=os.path.join(data_path,file_name)
      pp = pprint.PrettyPrinter(indent=4)
      with open(name_to_read, 'r') as f:
            df = pd.json_normalize(json.load(f))
      print("Read in {} rows and with {} variables".format(df.shape[0], df.shape[1]))
      print("  => First Timestamp: {}".format(df.iloc[0].server_timestamp))
      print("  => Last Timestamp : {}".format(df.iloc[-1].server_timestamp))
      names_payload=df.columns.values
      print(type(df[names_payload[0]].values))
      #np.savetxt('variable_names.txt',names_payload,fmt='%s')
      # filter out zeros or whatever you like.  Do this before extracting times to keep
      # the x/y arrays the same size.
      df = df[(df['payload.fAbsolutePressure'] != 0)]
      # the time that the data were sent to the server is in server_timestamp
      times = pd.to_datetime(df['server_timestamp'])
      return times, df

def load_SFC_lists(times,df):
      #examples to get the temps
      #lists go here, add Payton's stuff
      mainhsk_temps = df['payload.main_temps'].values
      DCT_temps = df['payload.dctThermistor'].values
      heliumLVL = df['payload.fMagnetHSK.heliumLevels']
      # to get just the first list element for each timestamp of the series...
      #mainhsk_temps_array=np.empty([len(mainhsk_temps),len(mainhsk_temps[0])])
      #temp_array=np.empty([len(mainhsk_temps[0]),])
      temp_list=[]
      for i in df['payload.fTOFStatus.fXadc'].values: temp_list.append(i)
      Xadc_array=np.asarray(temp_list)
      temp_list=[]
      for i in df['payload.fMagnetHSK.magnetFlows'].values: temp_list.append(i)
      magnetflows_array=np.asarray(temp_list)
      temp_list=[]
      for i in mainhsk_temps: temp_list.append(i)
      mainhsk_temps_array=np.asarray(temp_list)
      # now for DCT temps 
      temp_list=[]
      for i in DCT_temps: temp_list.append(i)
      DCT_temps_array=np.asarray(temp_list)
      #and helium levels
      temp_list=[]
      for i in heliumLVL: temp_list.append(i)
      helium_levels_array=np.asarray(temp_list)
      time_elapsed=pd.to_timedelta(times.values-times.values[0],unit='hours',errors="raise")
      time_deltas=time_elapsed/timedelta(hours=1) # can also do minutes
      return Xadc_array, magnetflows_array, mainhsk_temps_array, DCT_temps_array, helium_levels_array

def load_mainhsk_names(seq):
      mainhsk_names=pd.read_csv(os.path.join(data_path,'mainhsk_temp_sensors.txt'),engine='python')
      return mainhsk_names

def load_NASA_TCs(seq):
      # legend/order of loading csvs i guess
      NASA_names=pd.read_csv(os.path.join(data_path,"ATF_Data\\ATF_Data\\keith_final_legend_order.csv"))
      #print(NASA_names.ID.values[2])
      # NASA TCs loaded as a list first
      NASA_TCs=[]
      for name in NASA_names.ID:
          NASA_TCs.append(pd.read_csv(os.path.join(data_path,"ATF_Data\\ATF_Data\\"+name+"_csv.csv"),skiprows=1))
      # convert NASA times to timestamp proper
      #adjust to UTC like the other times
      time_change = timedelta(hours=5)
      for dfN in NASA_TCs:
          dfN['Times']=pd.to_datetime(dfN['Timestamp'])
          dfN['Times'] = dfN['Times'] + time_change
      return NASA_TCs, NASA_names

def load_minigoose(seq):
      #Load in minigoose temps
      minigoose_df=pd.read_csv(os.path.join(data_path,"MinigooseData\\MinigooseData.csv"))
      return minigoose_df

def load_mapping(seq):
      #load in mapping file
      #mapping_df=pd.read_csv(os.path.join(data_path,'HELIX_Thermal Information_for_python_csv.csv'),sep=',\s*',skipinitialspace=True,quoting=csv.QUOTE_ALL,engine='python')
      #mapping_df=pd.read_csv(os.path.join(data_path,'HELIX_Thermal Information_for_python_csv.csv'),sep=',\s*',quoting=csv.QUOTE_ALL,nrows=3,engine='python')
      mapping_df=pd.read_csv(os.path.join(data_path,'HELIX_Thermal Information_for_python_csv_v2_tabs.txt'), sep=';')
      return mapping_df

#load in all the variable names we want to plot
def load_var_names(seq):
      var_temp_names=pd.read_csv(os.path.join(data_path,'variable_names_temps_only.csv'))
      print("We will plot {} variables".format(len(var_temp_names.NAME.values)))
      return var_temp_names