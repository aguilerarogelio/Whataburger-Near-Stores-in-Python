#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
import csv
import random

def haversine(lat1, long1, lat2, long2):
    radiusOfEarthInMiles = 3958.8
    
    lat1Radians = math.radians(lat1)
    long1Radians = math.radians(long1)
    lat2Radians = math.radians(lat2)
    long2Radians = math.radians(long2)
    
    a = pow(math.sin((lat2Radians - lat1Radians) / 2), 2) + math.cos(lat1Radians) * math.cos(lat2Radians) * pow(math.sin((long2Radians - long1Radians) / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return radiusOfEarthInMiles * c

def random_partition(arr, low, high):
    random_index= random.randint(low, high)
    arr[high], arr[random_index] = arr[random_index], arr[high]
    pivot = arr[high][1]  
    i = low - 1
    
    for j in range(low, high):
        if arr[j][1]<=pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def random_select(arr,low,high,n):
    if low == high:
        return arr[low]
    
    pivot= random_partition(arr,low,high)
    rank = pivot  - low + 1
    
    if n == rank:
        return arr[pivot]
    elif n < rank:
        return random_select(arr, low, pivot- 1,n)
    else:
        return random_select(arr, pivot + 1,high, n-rank)

with open('queries.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader ) 
    for row in reader:
        query_lat, query_lon, n = map(float, row)
        n= int(n)
        stores = []
        with open('WhataburgerData.csv', newline='') as store_csvfile:
            store_reader = csv.reader(store_csvfile)
            next(store_reader ) 
            for store_row  in store_reader:
                store_id, address, city, state, zipcode, lat, lon = store_row[0], store_row[1], store_row[2], store_row[3], store_row[4], float(store_row[5]), float(store_row[6])
                stores.append((store_id, address, city, state, zipcode, haversine(lat, lon, query_lat, query_lon)))
        
        nth_closest_store = random_select(stores, 0, len(stores) - 1, n)
        nth_distance = nth_closest_store[0]
        
        closest_stores = [store for store in stores if store[1] <= nth_distance]
        
        closest_stores.sort(key=lambda x: x[5])
    
        print(f"The {n} closest stores to ({query_lat}, {query_lon}):")
        for i, (store_id, address, city, state, zipcode, distance) in enumerate(closest_stores[:n], 1):
            print(f"Store #{store_id}. {address}, {city}, {state}, {zipcode}. - {distance:.2f} miles.")
        print(" ")
            


# In[ ]:





# In[ ]:




