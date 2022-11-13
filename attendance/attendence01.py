#בס"ד
#Author : Tsibulsky David 309444065

import datetime
import pandas as pd
import numpy as np
import os

# assign directory with csv files :
#directory = 'attendance_csv_files'
directory = 'attendene2'

#init empty df for result
result = pd.DataFrame(columns=['Name','minutes'])
result2 = pd.DataFrame(columns=["Name"])
temp = pd.DataFrame(columns=["Name"])

total_minuts_of_all_lecturs = 0

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a csv file
    if os.path.isfile(f) and str(f).endswith(".csv"):
        #read csv file
        df = pd.read_csv(f, encoding= 'utf-16',engine='python', sep = '\t') #encoding= 'unicode_escape'

        #calculate  the lecture  duretion
        meeting_start_time = datetime.datetime.strptime(df["Meeting Start Time"][0][1:], '"%Y-%m-%d %H:%M:%S"')
        meeting_end_time = datetime.datetime.strptime(df["Meeting End Time"][0][1:], '"%Y-%m-%d %H:%M:%S"')
        timedelta_obj= meeting_end_time-meeting_start_time
        diff_in_minutes = timedelta_obj.total_seconds() / 60
        total_minuts_of_all_lecturs +=diff_in_minutes


        #create column with attendee duration in minutes , cast to integer
        df['minutes'] = df['Attendance Duration'].str.split(' ').str[0]
        df['minutes'] = df['minutes'].astype(int)




        #summarize all the entries of the same attendee
        df2 = df.groupby('Name').sum().reset_index()
        temp = pd.DataFrame(columns=["Name"])
        temp['Name'] = df2['Name']
        print("df2 >> ",str(f), df2['Name'], temp["Name"])
        temp[str(meeting_start_time)] = df2['minutes'].astype(str) +"min of " + str(round(diff_in_minutes,2)) + "min = " +((df2['minutes']/diff_in_minutes).round(2)).astype(str)+ "%"

        # temp[str(meeting_start_time)+" Lecture Duration"] = round(diff_in_minutes,2)
        # temp[str(meeting_start_time)+"  %Attendance time"] = (df2['minutes']/diff_in_minutes).round(2)
        # print("temp",len(temp.index))
        # temp.dropna(how="all",inplace=True)
        #
        # temp = temp.fillna(0)
        result2.dropna(how="all" ,inplace=True)
        result2 = pd.merge(temp,result2, on="Name", how="outer")
        print("result2 >>> ",len(result2.index))
        # temp.drop([str(meeting_start_time),"Name"], axis=1, inplace=True)
        # temp.drop(index="Name", inplace=True)
        #merge with a previous result
        result = pd.merge(result, df2, on="Name", how="outer")
        result = result.fillna(0)
        result["minutes"] = result["minutes_x"] + result["minutes_y"]
        result.drop(['minutes_x', 'minutes_y'], axis=1, inplace=True)


#arrange columns

print("result >> ",len(result.index))
result["Total lecture time (min)"] = round(total_minuts_of_all_lecturs,2)
result["% Attendance time"] = (result["minutes"]/total_minuts_of_all_lecturs).round(2)
result.rename(columns={"minutes":"Total atendance time (min)"},inplace=True)
result["More then 70% Attendence"] = np.where(result["% Attendance time"] >= 0.7 , "    YES", "    NO")

result2 = pd.merge(result2, result, on="Name", how="outer")

#save the result to csv file
result2.to_csv('output4.csv', index=False ,encoding = 'utf-8-sig')
