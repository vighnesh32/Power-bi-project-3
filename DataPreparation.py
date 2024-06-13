#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

file_path = 'events.xlsx'

# Load the Excel file using openpyxl
events_df = pd.read_excel(file_path, engine='openpyxl')

# Display the first few rows to understand the structure
events_df.head()


# In[2]:


# Check for null values in each column
null_summary = events_df.isnull().sum()
print("Null Values Summary:\n", null_summary)


# In[3]:


# Looking for number of unique event id
unique_eventid_count = events_df['eventid'].nunique()
unique_eventid_count


# In[4]:


# Replace null values in 'message' column with 'UNKNOWN'
events_df['message'] = events_df['message'].fillna('UNKNOWN')


# In[5]:


# Replace null values in 'severitykey' column with 'UNKNOWN'
events_df['severitykey'] = events_df['severitykey'].fillna('UNKNOWN')


# In[6]:


events_df.isnull().sum()


# In[7]:


# Convert the 'dhtimestamp' column from Unix epoch time to datetime
events_df['dhtimestamp'] = pd.to_datetime(events_df['dhtimestamp'], unit='ms', errors='coerce')

# Sort by objectid (unit) and timestamp
events_df = events_df.sort_values(by=['objectid', 'dhtimestamp'], ascending=True)

# Drop rows where latitude or longitude are null
events_df = events_df.dropna(subset=['gpslatitude', 'gpslongitude'])

# Get the most recent entry for each unit
most_recent_positions = events_df.groupby('objectid').tail(1)

# Select relevant columns
most_recent_positions = most_recent_positions[['objectid', 'dhtimestamp', 'gpslatitude', 'gpslongitude']]
most_recent_positions


# In[8]:


# Display the modified dataframe
events_df


# In[9]:


# Rechecking the null value
events_df.isnull().sum()


# In[10]:


import pandas as pd
import requests

def convert_to_three_words(latitude, longitude, api_key):
    url = "https://api.what3words.com/v3/convert-to-3wa"
    params = {
        "coordinates": f"{latitude},{longitude}",
        "key": api_key,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('words', 'No address found')
    elif response.status_code == 401:
        return "Error: Unauthorized. Please check your API key."
    elif response.status_code == 400:
        return "Error: Bad request. Please check the coordinates and parameters."
    else:
        return f"Error: {response.status_code}"

def get_place_name(latitude, longitude):
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        address = data.get('address', {})
        # Combine different parts of the address to form a place name
        place_name = ', '.join(filter(None, [
            address.get('road'),
            address.get('suburb'),
            address.get('city'),
            address.get('state'),
            address.get('country')
        ]))
        return place_name
    else:
        return f"Error: {response.status_code}"

# Sample data provided by the user
data = {
    'objectid': [
        'class707_707001', 'class707_707002', 'class707_707003', 'class707_707004', 'class707_707005', 
        'class707_707006', 'class707_707007', 'class707_707008', 'class707_707009', 'class707_707010', 
        'class707_707011', 'class707_707012', 'class707_707013', 'class707_707014', 'class707_707015', 
        'class707_707016', 'class707_707017', 'class707_707018', 'class707_707022', 'class707_707023', 
        'class707_707025', 'class707_707026', 'class707_707027', 'class707_707028', 'class707_707029', 
        'class707_707030'
    ],
    'dhtimestamp': [
        '2024-05-13 11:05:00.003', '2024-05-13 10:37:35.725', '2024-05-13 11:27:22.279',
        '2024-05-13 11:28:08.796', '2024-05-13 10:49:47.851', '2024-05-13 11:24:33.816',
        '2024-05-13 10:50:07.409', '2024-05-13 11:02:51.571', '2024-05-13 11:23:38.824',
        '2024-05-13 11:24:39.785', '2024-05-13 10:47:38.662', '2024-05-13 11:23:38.916',
        '2024-05-13 11:24:39.992', '2024-05-13 11:23:53.122', '2024-05-13 11:28:22.488',
        '2024-05-13 11:23:32.964', '2024-05-13 11:25:25.736', '2024-05-13 11:08:43.387',
        '2024-05-13 11:24:29.749', '2024-05-13 10:47:38.250', '2024-05-13 11:23:35.980',
        '2024-05-13 10:48:13.351', '2024-05-13 11:18:10.250', '2024-05-13 10:50:34.312',
        '2024-05-13 11:09:38.612', '2024-05-13 10:59:50.508'
    ],
    'gpslatitude': [51.463631, 51.464333, 51.444450, 51.461018, 51.470566, 51.438549, 51.472900, 51.475033, 51.464851, 51.463207, 51.441269, 51.433701, 51.462418, 51.438576, 51.373569, 51.463501, 51.465340, 51.474731, 51.439297, 51.441269, 51.432968, 51.470940, 51.470737, 51.473618, 51.373569, 51.501743],
    'gpslongitude': [0.194759, 0.193894, 0.006331, 0.197862, -0.025672, 0.011672, -0.029352, -0.031632, 0.193424, 0.194517, 0.367703, 0.018698, 0.195243, 0.011756, 0.089089, 0.194530, 0.193474, -0.031370, 0.010958, 0.366215, 0.019515, -0.026479, -0.026127, -0.030290, 0.089120, -0.112735]
}

# Convert the dictionary to a DataFrame
most_recent_positions = pd.DataFrame(data)

# what3words API key
api_key = 'HHQBXLOP'  # Replace with actual what3words API key

# Convert the most recent positions to three-word addresses and get place names
most_recent_positions['three_word_address'] = most_recent_positions.apply(
    lambda row: convert_to_three_words(row['gpslatitude'], row['gpslongitude'], api_key), axis=1
)
most_recent_positions['place_name'] = most_recent_positions.apply(
    lambda row: get_place_name(row['gpslatitude'], row['gpslongitude']), axis=1
)

# Display the results
most_recent_positions


# In[11]:


# Save the events_df DataFrame to an Excel file
events_df.to_excel('events_df.xlsx', index=False)

# Save the most_recent_positions DataFrame to an Excel file
most_recent_positions.to_excel('most_recent_positions.xlsx', index=False)


# In[ ]:




