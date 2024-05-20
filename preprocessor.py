

import pandas as pd
import regex as re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s..\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df.rename(columns={'message_date': 'date_time'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if len(entry) > 1:  # Ensure there's a username
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
          
        
    df['users'] = users
    df['message'] = messages
    df.drop(columns = ['user_message'], inplace = True )  

    df['dates'] = df['date_time'].str.split(',').str.get(0)
    df['time'] = df['date_time'].str.split(',').str.get(1)
    df['time'] = df['time'].str.split('-').str.get(0)
    
    df['dates'] = pd.to_datetime(df['dates'])
    df['day'] = df['dates'].dt.day
    df['month'] = df['dates'].dt.month_name()
    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month_name()
    df['day_name'] = df['dates'].dt.day_name()

    df['time'] = pd.to_datetime(df['time'], format=' %I:%M %p ')
    df['hour'] = df['time'].dt.hour
    df['minute'] = df['time'].dt.minute
    
    
    
    period = []
    for hour in df [['day_name' , 'hour']]['hour']:
        if hour ==23:
            period.append(str(hour) + "-" + str('00'))
        elif hour ==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    
    df['period'] = period

    df.drop(columns=('date_time'), inplace=True)
    
    return df   

    
    



