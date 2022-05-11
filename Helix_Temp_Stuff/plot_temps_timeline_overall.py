#!/usr/bin/python

import time
import pprint
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime, timedelta

from pip import main
print(os.getcwd())
print(os.path.dirname(__file__))
data_path=os.path.dirname(__file__)
file_name="Plum_Brook_Feb7_1400hr_to_End_Main\\Plum_Brook_Feb7_1400hr_to_End.json"
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
print(type(df['server_timestamp'].values[0]))
print(type(times[0]))
pressure  = df['payload.fAbsolutePressure']
sfc_temp  = df['payload.fSFCStatus.fCPU_Temp']
dini_temp = df['payload.fDiniTempFPGA']
richwest_power = df['payload.fPowerStat.fRICH_West.fPower']
dctboxtemp=df['payload.dctBoxTemp']
Magnet_probes=df['payload.fMagnetHSK.tempProbeAll']
#print(type(Magnet_probes.values))
#print(type(Magnet_probes.values[0]))
#print(Magnet_probes.values[0])

start_power=df.loc[df['payload.fPowerStat.fRICH_West.fPower']>100].index[0]
#start_power=times[df.iloc[df['payload.fPowerStat.fRICH_West.fPower']>100][0]]

mainhsk_temps  = df['payload.main_temps'].values
DCT_temps  = df['payload.dctThermistor'].values
heliumLVL=df['payload.fMagnetHSK.heliumLevels']

# to get just the first list element for each timestamp of the series...
#mainhsk_temps_array=np.empty([len(mainhsk_temps),len(mainhsk_temps[0])])
#temp_array=np.empty([len(mainhsk_temps[0]),])
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
mainhsk_names=pd.read_csv(os.path.join(data_path,'mainhsk_temp_sensors.txt'))
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

# Now make a plot
fig = plt.figure(figsize=(14, 10), dpi=200)
axs=fig.add_subplot(111)
#gs = fig.add_gridspec(1, 1)
#axs = gs.subplots(sharex=True, sharey=False)
#axs = gs.subplots()
#axs[0].scatter(times, pressure, marker='.')
#axs[0].set_ylabel("Pressure (Torr)")
#axs[0].set_ylim([1, 759])

# need timestamps to use here for cold wall begin filling and ending and then hot and cold cases respectively.
# datetime(year, month, day, hour, minute, second, microsecond)
#b = datetime(2017, 11, 28, 23, 55, 59, 342380)
cold_wall_fill_start = datetime(2022, 2, 7,21,0,0,0)
cold_wall_fill_end = datetime(2022, 2, 8,0,22,0,0)
power_on_DAQ = times[start_power]
cold_case_start=datetime(2022, 2, 8,1,6,0,0)
cold_case_end=datetime(2022, 2, 8,7,14,0,0)
hot_case_start=cold_case_end
hot_case_end=datetime(2022, 2, 8,17,30,0,0)
kickflip_start=hot_case_end
discharge_magnet = datetime(2022,2,8,20,35,0,0)
discharge_magnet_ps_off = datetime(2022,2,8,22,36,0,0)
drain_cold_wall_begin=datetime(2022,2,9,00,00,0,0)
#kickflip_end=datetime(2022, 2, 9,00,00,0,0) # not sure this actually stopped until during warm up
cold_wall_at_7ft=datetime(2022,2,9,4,00,0,0)
cold_wall_at_neg_6_deg=datetime(2022,2,9,7,37,0,0)
kickflip_end=datetime(2022,2,9,7,46,0,0)
slight_warmup_start=datetime(2022,2,9,10,52,0,0)
drain_cold_wall_end=datetime(2022,2,9,12,45,0,0)
slight_warmup_end=datetime(2022,2,9,12,45,0,0)
evacuation_start = datetime(2022,2,7,17,45,0,0)
evacuation_end = datetime(2022,2,9,17,00,0,0)
DAQ_Run = datetime(2022,2,8,5,41,0,0)
DAQ_Run_2 = datetime(2022,2,9,0,10,0,0)
heater_start=datetime(2022,2,8,13,18,0,0)
heater_max=datetime(2022,2,8,18,52,0,0)


# now in hours
# do conversions...

#Vertical lines
#axs[0].axvline(x=power_on_DAQ,ymin=0, ymax=1, color='red',label="power on DAQ")
#axs[0].text(power_on_DAQ, 10, "Power on DAQ", color='red',rotation=90, fontsize=8)
#axs[0].axvline(x=discharge_magnet,ymin=0, ymax=1, color='Brown',label="discharge magnet")
#axs[0].text(discharge_magnet, 10, "Discharge magnet", color='Brown', rotation=90, fontsize=8)
#axs[1].axvline(x=power_on_DAQ,ymin=0, ymax=1, ls=':', color='red')
#axs[1].axvline(x=discharge_magnet,ymin=0, ymax=1, ls=':',color='Brown')
#axs[1].axvline(x=cold_wall_fill_start,ymin=0, ymax=1, color='black',label="cold wall fill start")
#axs[1].axvline(x=cold_wall_fill_end,ymin=0, ymax=1, color='black',label="cold wall fill start")

# hatches for timespans
axs.axvspan(cold_wall_fill_start, cold_wall_fill_end, alpha=0.1, color='royalblue',label="cold wall fill")
axs.axvspan(cold_case_start, cold_case_end, alpha=0.1, color='cyan', label="cold case")
axs.axvspan(hot_case_start,hot_case_end , alpha=0.1, color='firebrick', label="hot case")
axs.axvspan(kickflip_start,kickflip_end , alpha=0.3, hatch="XXX", color='darkorange', label="flipped hot case")
axs.axvspan(drain_cold_wall_begin,drain_cold_wall_end , alpha=0.1, color='royalblue', label="draining cold wall")
axs.axvspan(slight_warmup_start,slight_warmup_end , alpha=0.3, color='red', label="slight warm up")

#size for markers visibility
s0=3
#temp data goes here

#across foam
#axs.scatter(NASA_TCs[1]['Times'], NASA_TCs[1]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[1]) # In South is on foam inside gondola
#axs.scatter(NASA_TCs[8]['Times'], NASA_TCs[8]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[8]) # SoLo is on foam outside gondola
#axs.scatter(NASA_TCs[0]['Times'], NASA_TCs[0]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[0]) # InEast is on foam inside foam
#axs.scatter(NASA_TCs[6]['Times'], NASA_TCs[6]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[6]) # EastLo is on foam inside gondola
#axs.set_ylim([-80, 30])
#axs.set_xlim([times.values[0],times.values[-1]])


#NASA TCs
iter=0
while iter<len(NASA_TCs):
    #print(len(NASA_TCs[iter]['Times'].values))
    #print(len(NASA_TCs[iter]['Value'].values))
    #print(NASA_names[iter]['Times'].values))
    axs.scatter(NASA_TCs[iter]['Times'], NASA_TCs[iter]['Value'], marker='.',s=s0,label=NASA_names.ID.values[iter]) # 
    iter+=1

axs.set_ylim([-79, 49])
axs.set_xlim([times.values[0],times.values[-1]])

# south here : seq=1
#axs.scatter(times, mainhsk_temps_array[:,7], marker='.',s=s0,label=mainhsk_names.Location.values[7]) # TOF top South
#axs.scatter(times, mainhsk_temps_array[:,5], marker='.',s=s0,label=mainhsk_names.Location.values[5]) # TOF btm south
#axs.scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) # gondola btm south
#axs.scatter(times, mainhsk_temps_array[:,8], marker='.',s=s0,label=mainhsk_names.Location.values[8]) # gondola mid South
#axs.scatter(NASA_TCs[13]['Times'], NASA_TCs[13]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[13]) # SoFr is on the gondola I believe
#axs.scatter(NASA_TCs[1]['Times'], NASA_TCs[1]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[1]) # In South is on foam inside gondola
#axs.scatter(NASA_TCs[7]['Times'], NASA_TCs[7]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[7]) # SoUp is on foam outside gondola
#axs.scatter(NASA_TCs[8]['Times'], NASA_TCs[8]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[8]) # SoUp is on foam outside gondola
#axs.set_ylim([-50, 33])
#axs.set_xlim([times.values[0],times.values[-1]])


#RICH east or west side
#axs.scatter(times, mainhsk_temps_array[:,13], marker='.',s=s0,label=mainhsk_names.Location.values[13]) # Mid east RICH heatsink
#axs.scatter(times, mainhsk_temps_array[:,17], marker='.',s=s0,label=mainhsk_names.Location.values[17]) # RICH cover E
#axs.scatter(NASA_TCs[0]['Times'], NASA_TCs[0]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[0]) # InEast is on foam inside foam
#axs.scatter(NASA_TCs[5]['Times'], NASA_TCs[5]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[5]) # EastUp is on foam inside gondola
#axs.scatter(NASA_TCs[6]['Times'], NASA_TCs[6]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[6]) # EastUp is on foam inside gondola
#axs.scatter(times, mainhsk_temps_array[:,14], marker='.',s=s0,label=mainhsk_names.Location.values[14]) # Mid West RICH heatsink
#axs.scatter(times, mainhsk_temps_array[:,19], marker='.',s=s0,label=mainhsk_names.Location.values[19]) # RICH cover E
#axs.scatter(NASA_TCs[9]['Times'], NASA_TCs[9]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[9]) # WestUp is on foam inside gondola
#axs.scatter(NASA_TCs[10]['Times'], NASA_TCs[10]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[10]) # WestLo is on foam inside gondola
#axs.set_ylim([-60, 60])
#axs.set_xlim([times.values[0],times.values[-1]])

#North side across foam
#correct/calibrate the North top TOF sensor
#begin_pumping=datetime(2022,2,7,14,55,0,0)
#times_calibrate=pd.to_datetime(times.values)
#times_range=np.asarray(begin_pumping-times_calibrate).astype('timedelta64[s]')
#times_range = times_range / np.timedelta64(1, 's')
#times_to_consider=np.where(times_range>0)
#TOF_diffs=mainhsk_temps_array[times_to_consider,21]-mainhsk_temps_array[times_to_consider,7]
#average_offset=np.mean(TOF_diffs[0])
#median_offset=np.median(TOF_diffs[0])
#axs.scatter(times, mainhsk_temps_array[:,20], marker='.',s=s0,label=mainhsk_names.Location.values[20]) # Gondola btm north
#axs.scatter(times, mainhsk_temps_array[:,16], marker='.',s=s0,label=mainhsk_names.Location.values[16]) # TOF btm N
#axs.scatter(times, mainhsk_temps_array[:,21]-average_offset, marker='.',s=s0,label=mainhsk_names.Location.values[21]) # TOF top N
#axs.scatter(NASA_TCs[3]['Times'], NASA_TCs[3]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[3]) # NoUp is on foam inside gondola
#axs.scatter(NASA_TCs[4]['Times'], NASA_TCs[4]['Value'], marker='2',s=s0,label="NASA TC - "+NASA_names.ID.values[4]) # NoLo is on foam inside gondola
#axs.set_ylim([-80, 30])
#axs.set_xlim([times.values[0],times.values[-1]])



#misc 1 interesting areas
#axs[1].scatter(times, mainhsk_temps_array[:,2], marker='.',s=s0,label=mainhsk_names.Location.values[2]) # DCT HV box
#axs[1].scatter(times, mainhsk_temps_array[:,6], marker='.',s=s0,label=mainhsk_names.Location.values[6]) # SFC backplate
#axs[1].scatter(times, mainhsk_temps_array[:,15], marker='.',s=s0,label=mainhsk_names.Location.values[15]) # Gas panel
#axs[1].scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) # gondola btm South
#axs[1].scatter(times, dctboxtemp, marker='.',s=s0,label="DCT box internal temp") # dctbox temp
#axs[1].set_ylim([-50, 38])


#RICH
#axs.axvline(x=DAQ_Run,ymin=0, ymax=1, color='red',label="DAQ Run")
#axs.axvline(x=DAQ_Run_2,ymin=0, ymax=1, color='black',label="DAQ Run 2 end")
#axs.scatter(times, mainhsk_temps_array[:,23], marker='.',s=s0,label=mainhsk_names.Location.values[23]) # rich focal plane NW
#axs.scatter(times, mainhsk_temps_array[:,0], marker='.',s=s0,label=mainhsk_names.Location.values[0]) # rich focal plane SW
#axs.scatter(times, mainhsk_temps_array[:,18], marker='.',s=s0,label=mainhsk_names.Location.values[18]) # rich cover N
#axs.scatter(times, mainhsk_temps_array[:,9], marker='.',s=s0,label=mainhsk_names.Location.values[9]) # rich cover S
#axs.scatter(times, mainhsk_temps_array[:,19], marker='.',s=s0,label=mainhsk_names.Location.values[19]) # rich cover W
#axs.scatter(times, mainhsk_temps_array[:,17], marker='.',s=s0,label=mainhsk_names.Location.values[17]) # rich cover E
#axs.set_ylim([-20, 39])

#TOF Fees only
#axs.scatter(times, mainhsk_temps_array[:,12], marker='.',s=s0,label=mainhsk_names.Location.values[12]) 
#axs.scatter(times, mainhsk_temps_array[:,22], marker='.',s=s0,label=mainhsk_names.Location.values[22]) 
#axs.scatter(times, mainhsk_temps_array[:,24], marker='.',s=s0,label=mainhsk_names.Location.values[24]) 
#axs.scatter(times, mainhsk_temps_array[:,25], marker='.',s=s0,label=mainhsk_names.Location.values[25]) 

#Gondola Bottom
#axs.scatter(times, mainhsk_temps_array[:,3], marker='.',s=s0,label=mainhsk_names.Location.values[3]) 
#axs.scatter(times, mainhsk_temps_array[:,4], marker='.',s=s0,label=mainhsk_names.Location.values[4]) 
#axs.scatter(times, mainhsk_temps_array[:,20], marker='.',s=s0,label=mainhsk_names.Location.values[20]) 
#axs.scatter(times, mainhsk_temps_array[:,2], marker='.',s=s0,label=mainhsk_names.Location.values[2])

#bore paddle stuff
#axs.scatter(times, mainhsk_temps_array[:,10], marker='.',s=s0,label=mainhsk_names.Location.values[10]) 
#axs.scatter(times, mainhsk_temps_array[:,11], marker='.',s=s0,label=mainhsk_names.Location.values[11]) 

#DCT
#axs.axvline(x=heater_start,ymin=0, ymax=1,ls='-', color='red',label="heaters start")
#axs.axvline(x=heater_max,ymin=0, ymax=1,ls=':', color='black',label="heaters highest")
#axs.scatter(times, mainhsk_temps_array[:,15], marker='.',s=s0,label=mainhsk_names.Location.values[15]) #gas panel
#axs.scatter(times, mainhsk_temps_array[:,1], marker='.',s=s0,label=mainhsk_names.Location.values[1])  # DCTV top
#dct box temp
#axs.scatter(times,df['payload.dctBoxTemp'], marker='2',s=s0,label="DCT HSK box uC") # In South is on foam inside gondola
#axs.set_ylim([-30, 50])
# for DCT thermistors
#iter=0
#while iter<len(DCT_temps[0]): #,label=mainhsk_names.Location.values[1]
#    axs[1].scatter(times, DCT_temps_array[:,iter], marker='.',s=s0)  # DCTV top
#    iter+=1
#
#axs[1].set_ylim([-20, 39])

axs.set_ylabel("Temps (C)")

plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d - %H:%M'))
plt.gcf().autofmt_xdate()
#axs[0].grid()
axs.grid()
#plt.legend(loc='upper center', fontsize=8)
handles, labels = axs.get_legend_handles_labels()
#lgd = axs[1].legend(handles, labels)
#for legend_handle in lgd.legendHandles:
#    legend_handle.set_sizes([20])
#labels[6]._legmarker.set_markersize(6)
lgd=fig.legend(handles, labels, loc='upper center', ncol=5, fontsize=8)
# as many of these as axs[1].scatter above


lgd.legendHandles[-14].set_sizes([60])
lgd.legendHandles[-13].set_sizes([60])
lgd.legendHandles[-12].set_sizes([60])
lgd.legendHandles[-11].set_sizes([60])
lgd.legendHandles[-10].set_sizes([60])
lgd.legendHandles[-9].set_sizes([60])
lgd.legendHandles[-8].set_sizes([60])
lgd.legendHandles[-7].set_sizes([60])
lgd.legendHandles[-6].set_sizes([60])
lgd.legendHandles[-5].set_sizes([60])
lgd.legendHandles[-4].set_sizes([60])
lgd.legendHandles[-3].set_sizes([60])
lgd.legendHandles[-2].set_sizes([60])
lgd.legendHandles[-1].set_sizes([60])#

#plt.savefig("plot_timeline_south.pdf", bbox_inches='tight')

#plt.savefig("plot_timeline_south.png")

plt.show()
