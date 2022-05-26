from datetime import datetime, timedelta

cold_wall_fill_start = datetime(2022, 2, 7,21,0,0,0)
cold_wall_fill_end = datetime(2022, 2, 8,0,22,0,0)
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
ColdestCase=[cold_wall_fill_start,cold_case_start]
ColdCase=[cold_case_start,cold_case_end]
HotCase=[hot_case_start,hot_case_end]
FlipCase=[kickflip_start,drain_cold_wall_begin]


def all_delta_times(seq):
      print("total times")
      print("__________________")
      print("Coldest case: {}".format(delta_times(ColdestCase)))
      print("Cold case: {}".format(delta_times(ColdCase)))
      print("Hot case: {}".format(delta_times(HotCase)))
      print("Flip case: {}".format(delta_times(FlipCase)))
      print("Cold Wall ON: {}".format(FlipCase[-1]-ColdCase[0]))

def delta_times(arg_array):
      return arg_array[-1]-arg_array[0]