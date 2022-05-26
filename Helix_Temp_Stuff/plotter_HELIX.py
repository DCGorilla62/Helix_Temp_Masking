import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import TVAC_time_constants as TVAC_times

def make_plot(x,y,name, y_range=None):
      s0=5
      fig = plt.figure(figsize=(14, 10), dpi=200)
      axs=fig.add_subplot(111)
      axs.scatter(x, y, marker='.',s=s0)  # DCTV top
      if y_range is not None:
            axs.set_ylim([y_range[-1], y_range[0]])
      #axs.set_ylim([-20, 39])
      plt.xticks(rotation=45)
      plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d - %H:%M'))
      plt.gcf().autofmt_xdate()
      #axs[0].grid()
      axs.grid()
      axs.set_ylabel("Temperature (C)",fontsize=12)
      plt.title(name)
      #plt.savefig(os.path.join(data_path,"plots_all\\"+names_payload[i]+".png"), bbox_inches='tight')
      plt.show()
        
        
def time_mask(timesx,seriesy,case_var):
      match case_var:
            case 'Coldest':
                  times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.ColdestCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.ColdestCase[-1]).to_datetime64())]
                  series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.ColdestCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.ColdestCase[-1]).to_datetime64())]
            case 'Cold':
                  times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.ColdCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.ColdCase[-1]).to_datetime64())]
                  series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.ColdCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.ColdCase[-1]).to_datetime64())]
            case 'Hot':
                  times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.HotCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.HotCase[-1]).to_datetime64())]
                  series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.HotCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.HotCase[-1]).to_datetime64())]
            case 'Flip':
                  times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.FlipCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.FlipCase[-1]).to_datetime64())]
                  series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.FlipCase[0]).to_datetime64()) &
                                       (timesx.values<=pd.to_datetime(TVAC_times.FlipCase[-1]).to_datetime64())]
      return times_masked,series_masked
#def time_mask(timesx,seriesy,case_var):
 #   if case_var == "Coldest":
  #      times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.ColdestCase[0]).to_datetime64()) &
   #                                    (timesx.values<=pd.to_datetime(TVAC_times.ColdestCase[-1]).to_datetime64())]
    #    series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.ColdestCase[0]).to_datetime64()) &
     #                                  (timesx.values<=pd.to_datetime(TVAC_times.ColdestCase[-1]).to_datetime64())]
    #elif case_var == 'Cold':
     #   times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.ColdCase[0]).to_datetime64()) &
      #                                 (timesx.values<=pd.to_datetime(TVAC_times.ColdCase[-1]).to_datetime64())]
       # series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.ColdCase[0]).to_datetime64()) &
        #                               (timesx.values<=pd.to_datetime(TVAC_times.ColdCase[-1]).to_datetime64())]
    #elif case_var == 'Hot':
     #   times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.HotCase[0]).to_datetime64()) &
      #                                 (timesx.values<=pd.to_datetime(TVAC_times.HotCase[-1]).to_datetime64())]
       # series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.HotCase[0]).to_datetime64()) &
        #                               (timesx.values<=pd.to_datetime(TVAC_times.HotCase[-1]).to_datetime64())]
    #elif case_var == 'Flip':
     #   times_masked=timesx.values[(timesx.values>=pd.to_datetime(TVAC_times.FlipCase[0]).to_datetime64()) &
      #                                 (timesx.values<=pd.to_datetime(TVAC_times.FlipCase[-1]).to_datetime64())]
       # series_masked=seriesy[(timesx.values>=pd.to_datetime(TVAC_times.FlipCase[0]).to_datetime64()) &
        #                               (timesx.values<=pd.to_datetime(TVAC_times.FlipCase[-1]).to_datetime64())]
    #return times_masked,series_masked