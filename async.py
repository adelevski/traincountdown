from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import requests
import time
import asyncio


TODAY = datetime.today()
OSTRING = "Western (O'Hare Branch)"

def extract_times(queue: list, element: ET):
    stop_name = element.find('eta').find('staNm').text
    # print(f"Next {stop_name} trains:")
    for i, train in enumerate(element.findall('eta')):
        time = train.find('arrT').text.split(' ')[-1]
        time = datetime.strptime(time, '%H:%M:%S').time()
        dt = datetime.combine(TODAY, time)
        queue.append([dt, stop_name])
        # print(f"#{i+1} - {time}")
    return queue

async def myCoroutine():
    while True:
        ro = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40670')
        rf = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key=97e711e0e761419e89d0ee28c76f0ef5&mapid=40220')
        ror = ET.fromstring(ro.text)
        rfr = ET.fromstring(rf.text)
        all_times = []

        all_times = extract_times(all_times, ror)
        all_times = extract_times(all_times, rfr)

        next_train = min(all_times, key=lambda x: x[0])
        next_train_time = next_train[0] - datetime.now() + timedelta(hours=0, minutes=0, seconds=20) if next_train[1] == OSTRING else next_train[0] - datetime.now() - timedelta(hours=0, minutes=0, seconds=20)
        next_train_direction = "O'Hare" if next_train[1] == OSTRING else 'FP'
        print(f"Next train in: {next_train_time} heading towards {next_train_direction}")
        await asyncio.sleep(5)


loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(myCoroutine())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Shutting Down.")
    loop.close()