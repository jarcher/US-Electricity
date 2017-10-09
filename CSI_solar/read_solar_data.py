import pandas as pd
import numpy as np
import matplotlib.pyplot as  plt

#Read in SGDE data files.
#Re-arrange as individual data series.
#Eventually output to SQL for easier access later.

nr=int(1E8)
try:
    if (len(df)!=nr):
        print('reusing old dataframe')
    else:
        print('df exists, but too short.  reloading')
        
        df = pd.read_csv('SDGE_StartThru2016Q3.zip',
                        nrows=nr,
                        usecols=['ID','LocalDateTime','kWh'])
except:
    print('df does not exist.  Loading from file')
    df = pd.read_csv('SDGE_StartThru2016Q3.zip',nrows=nr,\
                     usecols=['ID','LocalDateTime','kWh'])

#make time column to datetimes.

# #find unique names.
# for name in df['ID'].unique():
#     msk= df['ID']==name
#     d0 = 
#     times=df[msk,'LocalDateTime']
#     k

#for each name, make a time series. 

#Found that direct attempts to mask were taking way, way too long.
#Given structure in the data easier to find indices where the labels changed.

#find indices where names change (using fact series is grouped, in order)
def find_change(namevec,start,step=1000):
    end=len(namevec)
    pos=start
    old_name=namevec[start]
    while(namevec[pos]==old_name):
        pos_old=pos
        pos =pos+step
        if (pos >= end):
            print('hit end of vector, returning end')
            return end-1
        
    start_bkt=pos_old
    end_bkt=pos
    #now do bisection to search for change of index.
    start_name=namevec[start_bkt]
    end_name=namevec[end_bkt]
    while( (end_bkt-start_bkt)>1):
        mid=int((start_bkt+end_bkt)/2)
        mid_name=namevec[mid]
        if (start_name==mid_name):
            start_bkt=mid
            start_name=mid_name
        elif(end_name==mid_name):
            end_bkt=mid
            end_name=mid_name
    change_indx=end
    return end_bkt

#loop over entire list, finding all integer indices of all changes
def find_all_changes(namevec):
    change_vec=list();
    tot=len(namevec)-1;
    pos=0
    change_vec.append(pos)
    while (pos < tot):
        pos=find_change(namevec,pos)
        change_vec.append(pos)
        print(pos)
    change_vec=np.array(change_vec)
    return change_vec

#should use multiindex for datetimes.

#Now make existing dataframe into a list of time series.
def make_elec_series(df):
    indx_vec=find_all_changes(df['ID'])
    num_series=len(indx_vec)
    name_vec=df.loc[indx_vec,'ID']
    name_vec.index = range(num_series)
    ts_tot=list();
    #df_new=pd.DataFrame(columns=['ID','start','end','data'])
    tf='%d%b%y:%H:%M:%S'
    for i in range(num_series-1):
        name=name_vec[i]
        times=pd.to_datetime(df.loc[indx_vec[i]:indx_vec[i+1]-1,'LocalDateTime'],format=tf)
        # start_time=pd.to_datetime(df.loc[indx_vec[i],'LocalDateTime'],format=tf)
        # end_time=pd.to_datetime(df.loc[indx_vec[i+1]-1,'LocalDateTime'],format=tf)
        # # timeindex=pd.DatetimeIndex(start=start_time,end=end_time,freq='15 min')
        elec=df.loc[indx_vec[i]:indx_vec[i+1]-1,'kWh'].values
        ts = pd.Series(data=elec,index=times)
        ts_tot.append(ts)
    return ts_tot



#Now make existing dataframe into a list of time series.
def make_elec_series(df):
    indx_vec=find_all_changes(df['ID'])
    num_series=len(indx_vec)
    name_vec=df.loc[indx_vec,'ID']
    name_vec.index = range(num_series)
    ts_tot=list();
    #df_new=pd.DataFrame(columns=['ID','start','end','data'])
    tf='%d%b%y:%H:%M:%S'
    for i in range(num_series-1):
        name=name_vec[i]
        times=pd.to_datetime(df.loc[indx_vec[i]:indx_vec[i+1]-1,'LocalDateTime'],format=tf)
        # start_time=pd.to_datetime(df.loc[indx_vec[i],'LocalDateTime'],format=tf)
        # end_time=pd.to_datetime(df.loc[indx_vec[i+1]-1,'LocalDateTime'],format=tf)
        # # timeindex=pd.DatetimeIndex(start=start_time,end=end_time,freq='15 min')
        elec=df.loc[indx_vec[i]:indx_vec[i+1]-1,'kWh'].values
        ts = pd.Series(data=elec,index=times)
        ts_tot.append(ts)
    return ts_tot


df1= make_elec_series(df)

def plot_data(date,df):
    for s in df:
        try:plt.plot(s[date])
        except:print(date+' not found')
    plt.show()
    return

#When getting satellite data restrict from 5am-7pm.

#Randomly sample 10% of days as test set.

#Try to train simple model for total output on a given day.

#Simple questions:
# What is the seasonal variation?
#  * Could measure via average integrated power for a day, plot for whole dataset on yearly basis.
#  * Take weekly chunks to find variance.  For each sensor, take the mean over a particular week,
#   then plot the variance.
# How correlated are the data from different sensors?





