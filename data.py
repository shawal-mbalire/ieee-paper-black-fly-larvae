#load the file ieeepaper-default-rtdb-export.json 
import json


with open('ieeepaper-default-rtdb-export.json') as f:
    data = json.load(f)
    # convvvvert to dictionary
    data = dict(data)
    
# Access graph in data
graph = dict(data['graph']) # graph is a dictionary

lux =  dict(graph['lux']) # day lux time
temp =  dict(graph['temp']) # day temp time
hum =  dict(graph['hum']) # day hum time

# Access data in lux
for i in lux:
    #add values to lux.csv
    with open('lux.csv', 'a') as f:
        f.write(str(lux[i]['day']) + ',' + str(lux[i]['time']) + ',' + str(lux[i]['lux']) + '\n')

# Access data in temp
for i in temp:
    #add values to temp.csv
    with open('temp.csv', 'a') as f:
        f.write(str(temp[i]['day']) + ',' + str(temp[i]['time']) + ',' + str(temp[i]['tem']) + '\n')

# Access data in hum
for i in hum:
    #add values to hum.csv
    with open('hum.csv', 'a') as f:
        f.write(str(hum[i]['day']) + ',' + str(hum[i]['time']) + ',' + str(hum[i]['hum']) + '\n')



