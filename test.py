import xml.etree.ElementTree as ET
import requests
from datetime import datetime

ro = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40670')
rf = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40220')
ror = ET.fromstring(ro.text)
rfr = ET.fromstring(rf.text)
all_times = []
print(f"Next O'Hare Branch (Northwest) trains:")
today = datetime.today()
for i, train in enumerate(ror.findall('eta')):
    time = train.find('arrT').text.split(' ')[-1]
    time = datetime.strptime(time, '%H:%M:%S').time()
    dt = datetime.combine(today, time)
    all_times.append([dt, 'o'])
    print(f"#{i+1} - {time}")
print(f"Next FP Branch (Southeast) trains:")
for i, train in enumerate(rfr.findall('eta')):
    time = train.find('arrT').text.split(' ')[-1]
    time = datetime.strptime(time, '%H:%M:%S').time()
    dt = datetime.combine(today, time)
    all_times.append([dt, 'f'])
    print(f"#{i+1} - {time}")
next_train = min(all_times, key=lambda x: x[0])
next_train_time = next_train[0] - datetime.now()
next_train_direction = "O'Hare" if next_train[1] == 'o' else 'FP'
print(f"Next train in: {next_train_time} seconds heading towards {next_train_direction}")